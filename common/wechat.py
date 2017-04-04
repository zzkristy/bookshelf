import requests
import json
from common.conf import conf


class WechatService(object):
    URL_SESSION = 'https://api.weixin.qq.com/sns/jscode2session'

    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret

    def wx_get_session(self, code):
        data = {
            'appid': self.appid,
            'secret': self.appsecret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        r = requests.get(self.URL_SESSION, data)
        return json.loads(r.content.decode())


wechat_srv = WechatService(conf.wechat.appid, conf.wechat.appsecret)


if __name__ == "__main__":
    wechat_srv.wx_get_session('123456')
