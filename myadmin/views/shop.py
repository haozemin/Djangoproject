# 店铺信息视图文件
from django.shortcuts import render
from django.http import  HttpResponse
from django.core.paginator import  Paginator
from myadmin.models import Shop
from datetime import  datetime
import time
import random
# 封装或条件
# from django.db.models import Q
# 创建你的视图


def index(request,pindex=1):
    '''浏览信息'''
    slist =  Shop.objects.filter(status__lt=9)

    # 获取并判读搜索添加
    kw = request.GET.get("keyword",None)
    mywhere = []
    if kw:
        slist = slist.filter(name=kw)
        #维持搜索条件
        mywhere.append('keyword='+kw)



    # 执行分页处理
    pindex = int(pindex)
    page = Paginator(slist,5) #读取每页5条数据
    maxpage = page.num_pages #获取最大页数
    # 判断当前页是否越界
    if pindex > maxpage:
        pindex=maxpage
    elif pindex<1:
        pindex=1
    list2 = page.page(pindex) #获取当前页数据
    plist = page.page_range # 获取页码信息
    context = {'shoplist':list2,'plist':plist,'pindex':pindex,'maxpage':maxpage,'mywhere':mywhere}
    return render(request,"myadmin/shop/index.html",context)

def add(request):
    '''添加表单'''
    return render(request,'myadmin/shop/add.html')

def insert(request):
    '''执行添加'''
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # 实例化封装信息并执行添加操作
        ob=Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.status=1
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info':'添加成功'}
    except Exception  as err:
        context = {'info':'添加失败'}
    return render(request,'myadmin/info.html',context)

def delete(request,sid):
    '''删除'''
    try:
        ob = Shop.objects.get(id=sid)
        ob.status=9
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info':'删除成功'}
    except Exception  as err:
        context = {'info':'删除失败'}
    return render(request,'myadmin/info.html',context)

def edit(request,sid):
    '''编辑表单'''
    try:
        ob = Shop.objects.get(id=sid)
        context = {'shop':ob}
        print(ob.name)
        return render(request,'myadmin/shop/edit.html',context)
    except Exception  as err:
        context = {'info':'没有找到要修改的信息'}
        return render(request,'myadmin/info.html',context)

def update(request,uid):
    '''更新'''
    try:
        ob = Shop.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.adress = request.POST['adress']
        ob.phone = request.POST['phone']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '修改成功'}
    except Exception  as err:
        context = {'info': '修改失败'}
    return render(request, 'myadmin/info.html', context)