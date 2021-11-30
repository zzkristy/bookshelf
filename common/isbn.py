from common.mongo.service import isbn_srv
from common.qcloud import isbn_srv as qcloud_isbn_srv


def get_book(isbn):
    book = isbn_srv.get(isbn)
    if not book:
        content = qcloud_isbn_srv.fetch_book(isbn)
        if content["showapi_res_body"]["ret_code"] == 0:
            book = content["showapi_res_body"]["data"]
            isbn_srv.insert_one(isbn, book)
        else:
            raise Exception(content["showapi_res_body"]["remark"])
    return book
