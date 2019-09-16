import falcon

from lettergram.db_adapter import DBAdapter


class UserChatsGettingResource:
    def __init__(self, db_adapter: DBAdapter):
        self._db_adapter = db_adapter

    def on_post(self, req, resp):
        try:
            user_id = req.media['user']
            user_chats = list(self._db_adapter.get_user_chats(user_id=user_id))
            resp.media = [
                {
                    'id': str(chat.id),
                    'name': chat.name,
                    'users': list(chat.users),
                    'created_at': chat.created_at
                }
                for chat in user_chats
            ]
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPServiceUnavailable('Unknown error.', str(e))
