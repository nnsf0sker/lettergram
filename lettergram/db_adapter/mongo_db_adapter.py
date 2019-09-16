from typing import Set
from typing import Tuple
from typing import Optional

import pymongo
import datetime
from bson.objectid import ObjectId

from lettergram.models.user import User
from lettergram.models.chat import Chat
from lettergram.models.message import Message

from lettergram.db_adapter import DBAdapter


class MongoDBAdapterException(Exception):
    pass


class UsernameAlreadyIsUsedError(MongoDBAdapterException):
    def __init__(self, username: str):
        details = "Username '{username}' is already used.".format(username=username)
        super().__init__(details)


class ChatnameAlreadyIsUsedError(MongoDBAdapterException):
    def __init__(self, name: str):
        details = "Username '{name}' is already used.".format(name=name)
        super().__init__(details)


class AuthorNotInChatError(MongoDBAdapterException):
    def __init__(self, author_id: str, chat_id):
        details = "User '{author_id}' is not member of '{chat_id}' chat.".format(author_id=author_id, chat_id=chat_id)
        super().__init__(details)


class MongoDBAdapter(DBAdapter):
    def __init__(self, host: str, port: int):
        client = pymongo.MongoClient(host=host, port=port)
        db = client['avito-chat-db']
        self._users = db['users']
        self._chats = db['chats']
        self._messages = db['messages']

    def add_user(self, username: str) -> Optional[User]:
        created_at = str(datetime.datetime.now())
        if self._users.find_one({'username': username}):
            raise UsernameAlreadyIsUsedError(username=username)
        new_user = {
            'username': username,
            'created_at': created_at,
            'related_chats': []
        }
        user_adding_response = self._users.insert_one(new_user)
        new_user['id'] = str(user_adding_response.inserted_id)
        return User(
            id=new_user['id'],
            username=new_user['username'],
            created_at=new_user['created_at'],
            related_chats=tuple()
        )

    def add_chat(self, name: str, user_ids: Set[str]) -> Optional[Chat]:
        created_at = str(datetime.datetime.now())
        if self._chats.find_one({'name': name}):
            raise ChatnameAlreadyIsUsedError(name=name)
        new_chat = {
            'name': name,
            'users': user_ids,
            'created_at': created_at,
            'related_messages': []
        }
        chat_adding_response = self._chats.insert_one(new_chat)
        new_chat_id = str(chat_adding_response.inserted_id)
        new_chat['id'] = new_chat_id
        self._users.update_many(
            {'_id': {'$in': [ObjectId(id_) for id_ in user_ids]}},
            {'$push': {
                'related_chats': {
                    '$each': [new_chat_id],
                    '$position': 0,
                }
            }}
        )
        return Chat(
            id=new_chat['id'],
            name=new_chat['name'],
            users=frozenset(),
            created_at=new_chat['created_at'],
            related_messages=tuple()
        )

    def add_message(self, chat_id: str, author_id: str, text: str) -> Optional[Message]:
        created_at = str(datetime.datetime.now())
        chat_users = self._chats.find_one({'_id': ObjectId(chat_id)})['users']
        if author_id not in chat_users:
            raise AuthorNotInChatError(author_id=author_id, chat_id=chat_id)
        new_message = {
            'chat': chat_id,
            'author': author_id,
            'text': text,
            'created_at': created_at,
        }
        message_adding_response = self._messages.insert_one(new_message)
        new_message_id = str(message_adding_response.inserted_id)
        new_message['id'] = new_message_id
        self._chats.update_one(
            {'_id': ObjectId(chat_id)},
            {'$push': {
                'related_messages': {
                    '$each': [new_message_id],
                    '$position': 0,
                }
            }}
        )
        return Message(
            id=new_message['id'],
            chat=new_message['chat'],
            author=new_message['author'],
            text=new_message['text'],
            created_at=new_message['created_at']
        )

    def get_user_chats(self, user_id: str) -> Tuple[Chat, ...]:
        chat_ids = self._users.find_one({'_id': ObjectId(user_id)})['related_chats']
        result = []
        for chat_id in chat_ids:
            chat = self._chats.find_one({'_id': ObjectId(chat_id)})
            result.append(Chat(
                id=chat_id,
                name=chat['name'],
                users=chat['users'],
                created_at=chat['created_at'],
                related_messages=chat['related_messages']
            ))
        return tuple(result)

    def get_chat_messages(self, chat_id: str) -> Tuple[Message, ...]:
        message_ids = self._chats.find_one({'_id': ObjectId(chat_id)})['related_messages']
        print(message_ids)
        result = []
        for message_id in message_ids:
            message = self._messages.find_one({'_id': ObjectId(message_id)})
            result.append(Message(
                id=message_id,
                chat=message['chat'],
                author=message['author'],
                text=message['text'],
                created_at=message['created_at']
            ))
        return tuple(result)
