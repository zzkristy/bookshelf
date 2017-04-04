from pymongo import MongoClient

default_mongo_db = None


def config_mongo(conf):
    mongo_conf = conf.mongo
    global default_mongo_db
    if conf.get("test_env"):
        mongouri = 'mongodb://{}:{}/'.format(
            mongo_conf.host, int(mongo_conf.port)
        )
    else:
        mongouri = 'mongodb://{}:{}@{}:{}/{}'.format(
            mongo_conf.user,
            mongo_conf.password,
            mongo_conf.host,
            int(mongo_conf.port),
            mongo_conf.auth_db
        )
    conn = MongoClient(mongouri)
    default_mongo_db = conn[mongo_conf.name]


def sessionConn():
    global default_mongo_db
    return default_mongo_db['session']


def bookConn():
    global default_mongo_db
    return default_mongo_db['book']
