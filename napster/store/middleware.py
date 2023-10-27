from django.conf import settings

#
# class Basetest:
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self,request, *args, **kwargs):
#         print('start', self.middleware_name)
#
#         response = self.get_response(request)
#         print('end', self.middleware_name)
#
#
# class Test1(Basetest):
#     middleware_name = 'First'
#
# class Test2(Basetest):
#     middleware_name = 'second'
#
# class Test3(Basetest):
#     middleware_name = 'third'
#
#

class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.num_exceptions = 0
        self.num_req = 0
        self.context_response = {
            'msg': {'warning': 'There is no ink in the printer'}
        }

    def __call__(self,request, *args, **kwargs):
        print('Hello Middleware')
        response = self.get_response(request)
        self.num_req += 1
        print(f'Count of request receiver: {self.num_req}')

        print('path',request.path)
        print('host',request.headers['Host'])
        print('lang', request.headers['Accept-Language'])
        print('request_method',request.META['REQUEST_METHOD'])
        print('http useragent', request.META['HTTP_USER_AGENT'])
        print('http cookie', request.headers['Cookie'])

        if 'admin' not in request.path:
            self.stats(request.META['HTTP_USER_AGENT'])
        return response

    def stats(self, os_info):
        if 'Windows' in os_info:
            pass
        elif 'iphone' in os_info:
            pass
        else:
            pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f'view name:{view_func.__name__}')
        pass

    def process_exception(self, request, exception):
        self.num_exceptions += 1
        print(f'Exceptions count: {self.num_exceptions}')
        pass

    def process_template_responce(self, request, response):
        response.context_data['new_data'] = self.context_response
        print(response)
        return response






