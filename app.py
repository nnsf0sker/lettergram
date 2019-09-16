import falcon
from wsgiref import simple_server

from lettergram.db_adapter.mongo_db_adapter import MongoDBAdapter

from rest.user_adding_resource import UserAddingResource
from rest.chat_adding_resource import ChatAddingResource
from rest.message_adding_resource import MessageAddingResource
from rest.user_chats_getting_resource import UserChatsGettingResource
from rest.chat_messages_getting_resource import ChatMessagesGettingResource


def create_app():
    db_adapter = MongoDBAdapter(host='mongo', port=27017)

    user_adding_resource = UserAddingResource(db_adapter=db_adapter)
    chat_adding_resource = ChatAddingResource(db_adapter=db_adapter)
    message_adding_resource = MessageAddingResource(db_adapter=db_adapter)
    user_chats_getting_resource = UserChatsGettingResource(db_adapter=db_adapter)
    chat_messages_getting_resource = ChatMessagesGettingResource(db_adapter=db_adapter)

    api = falcon.API()
    api.add_route('/users/add', user_adding_resource)
    api.add_route('/chats/add', chat_adding_resource)
    api.add_route('/messages/add', message_adding_resource)
    api.add_route('/chats/get', user_chats_getting_resource)
    api.add_route('/messages/get', chat_messages_getting_resource)
    return api


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 9000
    httpd = simple_server.make_server(host, port, create_app())
    httpd.serve_forever()
