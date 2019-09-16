import falcon

from lettergram.db_adapter import DBAdapter


class ChatAddingResource:
    def __init__(self, db_adapter: DBAdapter):
        self._db_adapter = db_adapter

    def on_post(self, req, resp):
        try:
            name = req.media['name']
            users = req.media['users']
            made_chat = self._db_adapter.add_chat(name=name, user_ids=users)
            resp.media = {
                'id': made_chat.id,
            }
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPServiceUnavailable('Chat has not been created.', str(e))
