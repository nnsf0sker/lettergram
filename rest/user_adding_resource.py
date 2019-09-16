import falcon

from lettergram.db_adapter import DBAdapter


class UserAddingResource:
    def __init__(self, db_adapter: DBAdapter):
        self._db_adapter = db_adapter

    def on_post(self, req, resp):
        try:
            username = req.media['username']
            made_user = self._db_adapter.add_user(username=username)
            resp.media = {
                'id': made_user.id,
            }
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPServiceUnavailable('User has not been created', str(e))
