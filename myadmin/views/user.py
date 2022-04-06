# 员工信息视图文件
from django.shortcuts import render
from django.http import  HttpResponse
from django.core.paginator import  Paginator
from myadmin.models import User
from datetime import  datetime
import random
# 封装或条件
from django.db.models import Q
# 创建你的视图


def index(request,pindex=1):
    '''浏览信息'''
    ulist =  User.objects.filter(status__lt=9)

    # 获取并判读搜索添加
    kw = request.GET.get("keyword",None)
    mywhere = []
    if kw:
        ulist = ulist.filter(Q(username__contains=kw)|Q(nickname__contains=kw))
        #维持搜索条件
        mywhere.append('keyword='+kw)



    # 执行分页处理
    pindex = int(pindex)
    page = Paginator(ulist,5) #读取每页5条数据
    maxpage = page.num_pages #获取最大页数
    # 判断当前页是否越界
    if pindex > maxpage:
        pindex=maxpage
    elif pindex<1:
        pindex=1
    list2 = page.page(pindex) #获取当前页数据
    plist = page.page_range # 获取页码信息
    context = {'userlist':list2,'plist':plist,'pindex':pindex,'maxpage':maxpage,'mywhere':mywhere}
    return render(request,"myadmin/user/index.html",context)

def add(request):
    '''添加表单'''
    return render(request,'myadmin/user/add.html')

def insert(request):
    '''执行添加'''
    try:
        ob=User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        # 当前员工信心的密码做md5处理
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n) # 从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8')) # 将要产生的md5字串放进去
        ob.password_hash = md5.hexdigest()# 获取md5值
        ob.password_salt = n
        ob.status=1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info':'添加成功'}
    except Exception  as err:
        context = {'info':'添加失败'}
    return render(request,'myadmin/info.html',context)

def delete(request,uid):
    '''删除'''
    try:
        ob = User.objects.get(id=uid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info':'删除成功'}
    except Exception  as err:
        context = {'info':'删除失败'}
    return render(request,'myadmin/info.html',context)

def edit(request,uid):
    '''编辑表单'''
    try:
        ob = User.objects.get(id=uid)
        context = {'user':ob}
        print(ob.username)
        return render(request,'myadmin/user/edit.html',context)
    except Exception  as err:
        context = {'info':'没有找到要修改的信息'}
        return render(request,'myadmin/info.html',context)

def update(request,uid):
    '''更新'''
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '修改成功'}
    except Exception  as err:
        context = {'info': '修改失败'}
    return render(request, 'myadmin/info.html', context)