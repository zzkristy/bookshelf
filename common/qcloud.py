import hmac, base64, hashlib
from datetime import datetime as pydatetime
import requests
import json
from common.conf import conf


class ISBNService(object):
    def __init__(self, url, secretId, secretKey):
        self.url_isbn = url
        self.secretId = secretId
        self.secretKey = secretKey
        self.source = "market"

    def fetch_book(self, isbn):
        # 签名
        datetime = pydatetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        signStr = "x-date: %s\nx-source: %s" % (datetime, self.source)
        sign = base64.b64encode(
            hmac.new(
                self.secretKey.encode("utf-8"), signStr.encode("utf-8"), hashlib.sha1
            ).digest()
        )
        auth = (
            'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"'
            % (self.secretId, sign.decode("utf-8"))
        )
        # 请求头
        headers = {
            "X-Source": self.source,
            "X-Date": datetime,
            "Authorization": auth,
        }
        url = self.url_isbn + "?isbn={}".format(isbn)
        res = requests.get(url, headers=headers)
        content = json.loads(res.content.decode())
        return content


isbn_srv = ISBNService(conf.isbn.url, conf.isbn.secretId, conf.isbn.secretKey)

if __name__ == "__main__":
    content = isbn_srv.fetch_book("9787521734867")
    print(content)
