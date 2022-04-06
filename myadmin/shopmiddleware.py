# 自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse
import re
# 中间件
class ShopMiddleware:
    # 初始化类当前对象，只有服务启动是会被调用
    def __init__(self, get_response):
        self.get_response = get_response
        print('shopmiddleware')
        # One-time configuration and initialization.

    # 每次请求都会被调用
    def __call__(self, request):
        path = request.path
        print('url:',path)
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # 判断管理后台是否登录
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        # 判断当前请求url地址是否以/myadmin开头的,并且不在urllist中
        if re.match(r'^/myadmin',path) and (path not in urllist):
            # 判断是否登录(在session中没有adminuser则认为没有登录)
            if 'adminuser' not in  request.session:
                #重定向到登录页
                return  redirect(reverse('myadmin_login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response