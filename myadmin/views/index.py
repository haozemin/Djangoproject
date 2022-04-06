from django.shortcuts import render,redirect,reverse
from django.http import  HttpResponse
from myadmin.models import User
# 创建你的视图

import random
from PIL import Image, ImageDraw, ImageFont

# 后台管理员首页
def index(request):
    # return  HttpResponse("欢迎进入点餐系统的后台管理")
    return render(request,'myadmin/index/admin.html')

# 会员登录表单
def login(request):
    # return  HttpResponse("欢迎进入点餐系统的后台管理")
    return render(request,'myadmin/index/login.html')

# 执行会员登录
def dologin(request):
    # return  HttpResponse("欢迎进入点餐系统的后台管理")
    try:
        #执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            context = {'info': "验证码错误！！！"}
            return render(request, "myadmin/index/login.html", context)

        #     根据登录帐号获取登录信息
        user = User.objects.get(username = request.POST['username'])
        # 判断当前用户是否为管理员
        if user.status==6:
            # 获取密码并md5
            import hashlib
            md5 = hashlib.md5()
            n = user.password_salt
            s = request.POST['pass'] + str(n)
            md5.update(s.encode('utf-8'))
            # 校验密码是否正确
            if user.password_hash == md5.hexdigest():
                # 将当前登录成功用户信息以adminuser这个key放入到session中
                request.session['adminuser'] = user.toDict()
                return redirect(reverse('myadmin_index'))
            else:
                context = {"info": "登录密码错误！"}
        else:
            context = {"info": "此用户非后台管理账号！"}
    except Exception as err:
        print(err)
        context = {'info':"登录帐号不存在"}
    return render(request, "myadmin/index/login.html", context)

# 会员退出
def logout(request):
    # return  HttpResponse("欢迎进入点餐系统的后台管理")
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))


# 会员登录表单
def verify(request):
    #引入随机函数模块
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
