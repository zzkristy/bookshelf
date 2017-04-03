import redis

_redis_pool = None


def config_redis(conf):
    global _redis_pool
    redis_conf = conf.redis.session
    _redis_pool = redis.ConnectionPool(
        host=redis_conf.host,
        port=int(redis_conf.port),
        db=int(redis_conf.db),
        password=redis_conf.password
    )


def get_redis_client():
    global _redis_pool
    return redis.Redis(connection_pool=_redis_pool)
