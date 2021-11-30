from common.mongo.mongo_client import isbnConn
from datetime import datetime


class ISBNService(object):
    conn = isbnConn()

    def insert_one(self, isbn, data):
        book = self.conn.find_one({'isbn': isbn})
        if book:
            return
        data['isbn'] = isbn
        data['create_time'] = datetime.now()
        data['modify_time'] = datetime.now()
        self.conn.insert_one(data)

    def get(self, isbn):
        return self.conn.find_one({'isbn': isbn})
