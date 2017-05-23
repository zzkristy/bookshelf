import requests
import json
from datetime import datetime
from bookshelf.utils.views.common import CommonBaseView
from common.mongo.service import book_srv


class BookQueryView(CommonBaseView):

    def get(self, request):
        isbn = request.GET.get('isbn')
        if isbn:
            url = 'https://api.douban.com/v2/book/isbn/{}'.format(isbn)
            res = requests.get(url)
            content = json.loads(res.content.decode())
            result = {
                'isbn': isbn,
                'title': content['title'],
                'author': content['author'],
                'publisher': content['publisher'],
                'pubdate': content['pubdate'],
                'image': content['image'],
                'buydate': datetime.now().strftime('%Y-%m-%d'),
                'number': 1,
            }
            return self.JsonSuccessResponse(result)
        return self.JsonErrorResponse('请求参数有误')


class BookAddView(CommonBaseView):

    def post(self, request):
        try:
            data = request.POST
            isbn = data['isbn']
            content = {
                'title': data['title'],
                'author': data['author'],
                'publisher': data['publisher'],
                'pubdate': data['pubdate'],
                'image': data['image'],
                'buydate': datetime.strptime(data['buydate'], '%Y-%m-%d'),
                'number': int(data['number']),
                'remark': data.get('remark', '')
            }

            book_srv.insert_one(self.openid, isbn, content)
            return self.JsonSuccessResponse({'isbn': isbn})
        except KeyError:
            return self.JsonErrorResponse('请求参数有误')
        except Exception as e:
            return self.JsonErrorResponse(str(e))


class BookListView(CommonBaseView):

    def get(self, request):
        filters = {'user_id': self.openid}
        data = book_srv.find(filters)
        result = [{
            'isbn': d['isbn'],
            'title': d['title'],
            'author': d['author'],
            'publisher': d['publisher'],
            'pubdate': d['pubdate'],
            'image': d['image'],
        } for d in data]
        return self.JsonSuccessResponse(result)


class BookDetailView(CommonBaseView):

    def get(self, request):
        isbn = request.GET.get('isbn')
        book = book_srv.get(self.openid, isbn)
        result = {
            'isbn': book['isbn'],
            'title': book['title'],
            'author': book['author'],
            'publisher': book['publisher'],
            'pubdate': book['pubdate'],
            'image': book['image'],
            'buydate': book['buydate'].strftime('%Y-%m-%d'),
            'number': book['number'],
            'remark': book.get('remark', '')
        }
        return self.JsonSuccessResponse(result)
