from functools import update_wrapper
from django.views.generic import View
from common.wechat import wechat_srv
from django.http.response import JsonResponse


class LoginView(View):

    def get(self, request):
        code = request.GET.get('code')
        if code:
            result = wechat_srv.wx_get_session(code)
            if 'openid' in result:
                request.session['openid'] = result['openid']
                request.session['session_key'] = result['session_key']
                request.session.save()
                return JsonResponse({'code': 0, 'data': request.session.session_key})
            else:
                return JsonResponse({'code': 1, 'msg': result.get('errmsg', '')})
        return JsonResponse({'code': 1, 'msg': '缺少code参数'})


class AjaxNoLoginView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "code": 100,
            "msg": '没有登录',
            "data": None
        }, status=200)

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "code": 100,
            "msg": '没有登录',
            "data": None
        }, status=200)


class BasePermitView(View):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.request_method = request.method.lower()

    @classmethod
    def as_view(cls, **initkwargs):
        _inner_view = cls._inner_view_(**initkwargs)

        def view(request, *args, **kwargs):
            target_view = _inner_view
            if not request.session.get('openid'):
                target_view = AjaxNoLoginView.as_view()
            return target_view(request, *args, **kwargs)
        return view

    @classmethod
    def _inner_view_(cls, **initkwargs):
        def view(request, *args, **kwargs):
            self = cls(request=request, **initkwargs)
            self.args = args
            self.kwargs = kwargs

            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            if self.request_method in self.http_method_names:
                handler = getattr(
                    self, self.request_method, self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            return handler(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        return view
