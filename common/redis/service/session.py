from ..redis_client import get_redis_client


class SessionService(object):
    c = get_redis_client()
    prefix = 'session_'

    def _get_key_(self, session_key):
        return self.prefix + str(session_key)

    def get(self, session_key):
        real_key = self._get_key_(session_key)
        return self.c.get(real_key)

    def set(self, session_key, data, expiry_age):
        self.c.set(self._get_key_(session_key), data)
        self.c.expire(self._get_key_(session_key), expiry_age)

    def exists(self, session_key):
        real_key = self._get_key_(session_key)
        return self.c.exists(real_key)

    def delete(self, session_key):
        real_key = self._get_key_(session_key)
        return self.c.delete(real_key)
