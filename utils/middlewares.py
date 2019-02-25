from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect,HttpResponse

class Authmiddleware(MiddlewareMixin):

    def process_request(self,request):
        # 判断白名单
        print(request.path)  #  /路由/
        if request.path in ["/login/",'/get_valid_img/','/register/']:
            # 放行
            return None
        print(request.user.is_authenticated)  # /login/
        if not request.user.is_authenticated:
            return redirect("/login/")

class Dontvisit(MiddlewareMixin):

    def process_request(self,request):
        visit_list =['127.0.0.1']
        path = request.META.get('REMOTE_ADDR')
        print(path)
        if path not in visit_list :
            return HttpResponse('无法访问')