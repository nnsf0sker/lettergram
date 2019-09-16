import falcon

from lettergram.db_adapter import DBAdapter


class ChatMessagesGettingResource:
    def __init__(self, db_adapter: DBAdapter):
        self._db_adapter = db_adapter

    def on_post(self, req, resp):
        try:
            chat_id = req.media['chat']
            chat_messages = list(self._db_adapter.get_chat_messages(chat_id=chat_id))
            resp.media = [
                {
                    'id': message.id,
                    'chat': message.chat,
                    'author': message.author,
                    'text': message.text,
                    'created_at': message.created_at
                }
                for message in chat_messages
            ]
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPServiceUnavailable('Unknown error.', str(e))
