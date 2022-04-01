# class MyAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#
#         response = self.get_response(request)
#
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response
#
#     # process_view(), process_exception(), process_template_response()
#     # special methods to class-based middleware
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # process_view() is called just before Django calls the view.
#         # It should return either None or an HttpResponse object
#         # todo: check this mdfk
#         token = request.META.get("HTTP_AUTHORIZATION")
#         if token is None:
#             return None
#         # print(token)
#         return None
