from common.mongo.mongo_client import sessionConn
from datetime import datetime, timedelta


class SessionService(object):
    conn = sessionConn()

    def get(self, session_key):
        filters = {
            'session_key': session_key,
            'expiry_date': {'$gt': datetime.now()}
        }
        return self.conn.find_one(filters)

    def set(self, session_key, data, expiry_age):
        expiry_date = datetime.now() + timedelta(seconds=expiry_age)
        self.conn.update(
            {'session_key': session_key},
            {'$set': {'session_data': data, 'expiry_date': expiry_date}},
            upsert=True
        )

    def exists(self, session_key):
        return self.get(session_key)

    def delete(self, session_key):
        self.conn.delete_one({'session_key': session_key})
