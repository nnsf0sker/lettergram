import falcon

from lettergram.db_adapter import DBAdapter


class MessageAddingResource:
    def __init__(self, db_adapter: DBAdapter):
        self._db_adapter = db_adapter

    def on_post(self, req, resp):
        try:
            chat_id = req.media['chat']
            author_user_id = req.media['author']
            text = req.media['text']
            made_message = self._db_adapter.add_message(chat_id=chat_id, author_id=author_user_id, text=text)
            resp.media = {
                'id': made_message.id,
            }
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPServiceUnavailable('Message has not been created.', str(e))
