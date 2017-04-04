import json
from logging import getLogger
from .base import BasePermitView
from .ajax import FormAjaxResponseMixin

logger = getLogger('access')


class CommonBaseView(BasePermitView, FormAjaxResponseMixin):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.openid = request.session.get('openid')
        self.log_request(request)

    def log_request(self, request):
        logger.info(self.request_method.upper() + ' ' + request.path)
        logger.info('request_user:: id:{}'.format(self.openid))
        data = None
        if self.request_method == 'post':
            data = request.POST.dict()
        elif self.request_method == 'get':
            data = request.GET.dict()
        logger.info(self.request_method.upper() + '_DATA:{}'.format(json.dumps(data)))
