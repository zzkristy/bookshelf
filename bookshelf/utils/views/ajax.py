from django.http import JsonResponse


class FormAjaxResponseMixin():

    def JsonFormErrorResponse(self, form, msg='', status=400):
        error_data = {
            "code": 2,
            "msg": msg,
            "error": form.errors
        }
        return JsonResponse(error_data, status)

    def JsonErrorResponse(self, msg='', data=None, code=1, status=200):
        return JsonResponse({
            "code": code if code != 0 else 1,
            "msg": msg,  # 简短错误描述
            "data": data
        }, status=status)

    def JsonSuccessResponse(self, data_dict=None, msg="ok", pagination={}):
        result_data = {
            "code": 0,
            "msg": msg,
            "data": data_dict,
        }
        # 分页信息
        # pagination = {'count': count, 'offset': offset, 'limit': limit}
        if pagination:
            result_data['pagination'] = pagination
        return JsonResponse(result_data)

    def JsonResponse(self, data, msg="", code=0, status=200):
        result_data = {
            "code": code,
            "msg": msg,
            "data": data,
        }
        return JsonResponse(result_data)

    def directJson(self, data):
        assert type(data) is dict
        return JsonResponse(data)

    def directList(self, data):
        assert type(data) is list
        return JsonResponse(data, safe=False)
