from django.shortcuts import render
from django.core   import serializers
import markdown
import json
from django.http import HttpResponse

from .models import User, Device, UserDevice, DeviceLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 导入分页插件包
import requests


def global_variable(request):
    #rightTui = Article.objects.filter(tui__id=2)[:6]
    #alltags = Tag.objects.all()
    #allcategory = Category.objects.all()
    return locals()

def index(request):
    # hot = Article.objects.all().order_by('?')[:10] # 随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10]   # 通过自定义推荐进行查询，以推荐ID是3为例
    json_data = serializers.serialize("json", {'a':'AAAAAAAAAAAAAA'})
    return HttpResponse(json_data,content_type="application/json")

def getOpenId(request):
    code = request.GET['code']
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid=wxef0519d42d63eaf7&secret=8ac05353cf3caf74c80e47db9dc01c67&js_code='+code+'&grant_type=authorization_code')
    res = json.loads(r.text)
    if 'openid' not in res:
        return HttpResponse(json.dumps({'res':False}),content_type="application/json")
    print('####openid:',res['openid'])
    return HttpResponse(json.dumps({
        'res':True,
        'openid':res['openid']
        }),content_type="application/json")

def bindPhone(request):
    openid = request.GET['openid']
    phone = request.GET['phone']
    print(phone, openid)
    if not openid or not phone:
        return HttpResponse(json.dumps({'res':False}),content_type="application/json")
    user = User(phone=phone, open_id=openid, img='init_image')
    user.save()
    return HttpResponse(json.dumps({
        'res':True,
        'openid':openid,
        'phone':phone
        }),content_type="application/json")

def addDevice(request):
    device_id = Device.objects.get(serial_num=request.GET['serial_num'])
    phone = User.objects.get(phone=request.GET['phone'])
    print({
        'res':True,
        'serial_num':request.GET['serial_num'],
        'source':request.GET['source'],
        'phone':request.GET['phone']
        })
    # 第一个绑定的作为管理员
    if not UserDevice.objects.filter(device_id=device_id).exists():
        device_id.adm_phone = phone
        device_id.save()

    userdevice = UserDevice(
            phone = phone,
            device_id = device_id,
            remark_name = 'newDevice',
            source = int(request.GET['source']) # 0/1
            )
    userdevice.save()
    return HttpResponse(json.dumps({
        'res':True,
        'serial_num':request.GET['serial_num'],
        'phone':request.GET['phone']
        }),content_type="application/json")
    


def delDevice(request):
    device_id = Device.objects.get(device_id=request.GET['device_id'])
    phone = User.objects.get(phone=request.GET['phone'])
    querySet = UserDevice.objects.filter(
            phone = phone,
            device_id = device_id
            )
    exists = querySet.exists()
    querySet.delete()
    # if len(ud):
        # for i in ud:
            # i.delete()
    return HttpResponse(json.dumps({
        'res':True,
        'exists':exists,
        'serial_num':request.GET['device_id'],
        'phone':request.GET['phone']
        }),content_type="application/json")


def userDevices(request):

    deviceid_list = [{
        'device_id':device.device_id.device_id,
        'remark_name':device.remark_name}
        for device in UserDevice.objects.filter(phone=request.GET['phone'])]
    for d in deviceid_list:
        device = Device.objects.get(device_id=d['device_id'])
        d['name'] = device.name
        d['serial_num'] = device.serial_num
        d['admin'] = device.adm_phone.phone
    return HttpResponse(json.dumps({
        'res':True,
        'phone':request.GET['phone'],
        'deviceid_list':deviceid_list
        }),content_type="application/json")




def userDevice(request):
    device = Device.objects.get(device_id=request.GET['device_id'])
    deviceInfo = {
            'device_id':request.GET['device_id'],
            'name': device.name,
            'openDegree': device.position,
            'error': device.error
            }
    # 如果是管理员的话

    if device.adm_phone.phone == request.GET['phone']:
        deviceInfo['admin'] = 'Myself'
    return HttpResponse(json.dumps({
        'res':True,
        'phone':request.GET['phone'],
        'device':deviceInfo
        }),content_type="application/json")


def openDegree(request):
    ctrl = False
    device_id = Device.objects.get(device_id=request.GET['device_id'])
    phone = User.objects.get(phone=request.GET['phone'])
    ud = UserDevice.objects.get(device_id=device_id,phone=phone)
    if device_id.access_ctrl == 0:
        ctrl = True
    elif ud.a_access or ud.p_access:
        ctrl = True

    if ctrl:
        device_id.position = int(request.GET['number'])
        device_id.save()
        return HttpResponse(json.dumps({
            'res':True,
            'phone':request.GET['phone'],
            'ctrlRight':True,
            'modified':True
            }),content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'res':True,
            'phone':request.GET['phone'],
            'ctrlRight':False,
            'modified':False
            }),content_type="application/json")

# 接收POST请求数据

def test(request):
    name = "hello haiyan"
    value="<div href=\"\">点击</div>"
    i = 200
    l = [11,22,33,44,55]
    d = {"name":"haiyan","age":20}

    class People(object): #继承元类
        def __init__(self,name,age):
            self.name = name
            self.age = age
        def __str__(self):
            return self.name+str(self.age)
        def dream(self):
            return "你有梦想吗？"
    #实例化
    person_egon = People("egon",10)
    person_dada = People("dada",34)
    person_susan = People("susan",34)
    person_list = [person_dada,person_egon,person_susan]

    return render(request,"test.html",
                    {
                        "name":name,
                        "i":i,
                        "l":l,
                        "d":d,  #键对应的是模板里的名字。值对应的是上面定义的变量
                        "person_egon":person_egon,
                        "person_dada":person_dada,
                        "person_list":person_list,
                    }
              )
    # return render(request,"index.html",locals())
    #用locals()可以不用写上面的render了。不过用locals()，views里面用什么名。模板里面就得用什么名
    # locals()局部的：用了locals就相当于都得按照上面的那样





# 首页
