from common.mongo.mongo_client import bookConn
from datetime import datetime


class BookService(object):
    conn = bookConn()
    status_normal = 2
    status_deleted = 1

    def insert_one(self, user_id, isbn, data):
        book = self.conn.find_one({'user_id': user_id, 'isbn': isbn})
        if book:
            raise Exception('书籍已存在')
        data['user_id'] = user_id
        data['isbn'] = isbn
        data['create_time'] = datetime.now()
        data['modify_time'] = datetime.now()
        data['status'] = self.status_normal
        self.conn.insert_one(data)

    def find(self, filters):
        filters['status'] = self.status_normal
        return self.conn.find(filters)

    def get(self, user_id, isbn):
        return self.conn.find_one({'user_id': user_id, 'isbn': isbn})
