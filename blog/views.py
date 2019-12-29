from django.shortcuts import render
from django.core   import serializers
#import markdown
import json
import inspect
from django.http import HttpResponse

from .models import User, Device, UserDevice, DeviceLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 导入分页插件包
import requests
import random

def getDeviceRight(phone,userDevice):
    '''
    获得权限等信息
    '''
    device = userDevice.deviceId
    deviceRight = {}
    deviceRight['deviceId'] = device.deviceId
    deviceRight['name'] = device.name
    deviceRight['serialNum'] = device.serialNum
    deviceRight['remarkName'] = userDevice.remarkName
    deviceRight['admin'] = False
    deviceRight['ctrl'] = False
    # 管理员账户
    if device.adminPhone.phone == phone:
        deviceRight['admin'] = True
        deviceRight['ctrl'] = True
    # 未启用访问权限
    if device.accessCtrl == 0:
        deviceRight['ctrl'] = True
    # 有控制权限
    if userDevice.aAccess or userDevice.pAccess:
        deviceRight['ctrl'] = True

    return deviceRight


def getDeviceLog(device):
    '''
    获得设备日志
    '''
    return [ {
        'time':log.logTime.strftime('%Y-%m-%d %H:%M:%S'),
        'type':log.logType,
        'content':log.logContent
        }
        for log in DeviceLog.objects.filter(deviceId=device)
        ]

def getDeviceInfo(device):
    '''
    获得设备信息
    '''
    return {
            'position':device.position,
            'ioState':device.ioState,
            'accuracy':device.accuracy,
            'state':device.state,
            'network':device.network,
            'error':device.error
            }


def getDeviceConfig(device,userDevice):
    '''
    获得设备配置信息
    '''
    res = {
            'admin':device.adminPhone.phone,
            'name':device.name,
            'remarkName':userDevice.remarkName,
            'serialNum':device.serialNum,
            'remark':device.remark,
            'accessCtrl':device.accessCtrl,
            'password':device.cPass,

            # TODO: 用户权限管理
            'source':userDevice.source,
            'aAccess':userDevice.aAccess,
            'pAccess':userDevice.pAccess
            }
    if userDevice.source == 2:
        res['aPhone'] = userDevice.aPhone.phone
    return res



def global_variable(request):
    #allcategory = Category.objects.all()
    return locals()

def index(request):
    # hot = Article.objects.all().order_by('?')[:10] # 随机推荐
    # hot = Article.objects.filter(tui__id=3)[:10]   # 通过自定义推荐进行查询，以推荐ID是3为例
    json_data = serializers.serialize("json", {'a':'AAAAAAAAAAAAAA'})
    return HttpResponse(json_data,content_type="application/json")

def registerDevice(request):
    '''
    注册设备
    '''
    serialNum = request.GET['serialNum']
    name = request.GET['name']
    remark = request.GET['remark']

    accessCtrl = 0
    cPass = '123'

    position = random.randint(0,100)
    ioState = random.randint(0,1)
    accuracy = random.randint(0,100)
    state = random.randint(0,1)
    network = random.randint(0,1)
    error = random.randint(0,5)

    device = Device(
            serialNum = serialNum,
            name = name,
            remark = remark,

            accessCtrl = accessCtrl,
            cPass = cPass,

            position = position,
            ioState = ioState,
            accuracy = accuracy,
            state = state,
            network = network,
            error = error
            )
    device.save()

    # json_data = serializers.serialize("json", device)
    # print(device)
    # print(json_data)
    # return HttpResponse('{"name":"hahha"}',content_type="application/json")
    return HttpResponse(json.dumps({
        'res':True
        }),content_type="application/json")


## getOpenId| code|openid
def getOpenId(request):
    '''
    获取openid
    '''
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


## bindPhone|openid,phone|res
def bindPhone(request):
    '''
    绑定手机和openid
    '''
    openid = request.GET['openid']
    phone = request.GET['phone']
    print(phone, openid)
    if not openid or not phone:
        return HttpResponse(json.dumps({'res':False}),content_type="application/json")
    user = User(phone=phone, openId=openid)
    user.save()
    return HttpResponse(json.dumps({
        'res':True,
        'openid':openid,
        'phone':phone
        }),content_type="application/json")

## addDevice|phone,serialNum,source|deviceList
def addDevice(request):
    '''
    用户添加设备
    '''
    deviceId = Device.objects.get(serialNum=request.GET['serialNum'])
    phone = User.objects.get(phone=request.GET['phone'])
    # 第一个绑定的作为管理员
    if not UserDevice.objects.filter(deviceId=deviceId).exists():
        deviceId.adminPhone = phone
        deviceId.save()

    userdevice = UserDevice(
            phone = phone,
            deviceId = deviceId,
            remarkName = 'newDevice',
            source = int(request.GET['source']) # 0/1
            )
    userdevice.save()
    return userDevices(request)
    


## delDevice|phone,deviceId|deviceList
def delDevice(request):
    deviceId = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    querySet = UserDevice.objects.filter(
            phone = phone,
            deviceId = deviceId
            )
    exists = querySet.exists()
    querySet.delete()
    return userDevices(request)


## userDevices|phone|deviceList
def userDevices(request):
    deviceList = []
    phone = request.GET['phone']
    for ud in UserDevice.objects.filter(phone=phone):
        deviceList.append(getDeviceRight(phone, ud))

    return HttpResponse(json.dumps({
        'res':True,
        'deviceList':deviceList
        }),content_type="application/json")


## userDeviceInfo|deviceId|deviceInfo
def userDeviceInfo(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    return HttpResponse(json.dumps({
        'res':True,
        'deviceInfo':getDeviceInfo(device)
        }),content_type="application/json")

## userDeviceConfig|deviceId|deviceConfig
def userDeviceConfig(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    ud = UserDevice.objects.get(deviceId=device,phone=phone)
    return HttpResponse(json.dumps({
        'res':True,
        'deviceConfig':getDeviceConfig(device,ud)
        }),content_type="application/json")

## deviceInfoCtrl|deviceId,phone,xxx|deviceInfo/deviceConfig
def deviceInfoCtrl(request):
    print("=========================================")
    print("=========================================")
    ctrl = False
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    ud = UserDevice.objects.get(deviceId=device,phone=phone)

    DeviceLog(deviceId=device,
            logType=0,
            logContent='P:%s %s'%(request.GET['phone'],inspect.stack()[0][3])).save()
    
    if 'remarkName' in request.GET:
        ud.remarkName = request.GET['remarkName']
        ud.save()
        return HttpResponse(json.dumps({
            'res':True,
            'deviceConfig':getDeviceConfig(device,ud)
            }),content_type="application/json")

    if 'position' in request.GET:
        device.position = int(request.GET['position'])
    elif 'ioState' in request.GET:
        device.ioState = int(request.GET['ioState'])
    elif 'accuracy' in request.GET:
        device.accuracy = int(request.GET['accuracy'])
    elif 'name' in request.GET:
        device.name = request.GET['name']
    elif 'remark' in request.GET:
        device.remark = request.GET['remark']
    device.save()

    return HttpResponse(json.dumps({
        'res':True,
        'deviceInfo':getDeviceInfo(device)
        }),content_type="application/json")


## startAccessCtrl|deviceId|device
def startAccessCtrl(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    ud = UserDevice.objects.get(deviceId=device,phone=phone)
    device.accessCtrl = True
    device.save()
    return HttpResponse(json.dumps({
        'res':True,
        'deviceConfig':getDeviceConfig(device,ud)
        }),content_type="application/json")

## updatePassword|deviceId,password|deviceConfig
def updatePassword(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    ud = UserDevice.objects.get(deviceId=device,phone=phone)
    device.cPass = request.GET['password']
    device.save()
    for ud in UserDevice.objects.filter(deviceId=device):
        ud.pAccess = 0
        ud.save()

    return HttpResponse(json.dumps({
        'res':True,
        'deviceConfig':getDeviceConfig(device,ud)
        }),content_type="application/json")


## deviceLog|deviceId|log
def deviceLog(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    return HttpResponse(json.dumps({
        'res':True,
        'log':getDeviceLog(device)
        }),content_type="application/json")


## addAccessRight|deviceId,phone,aPhone|deviceConfig,deviceRight
def addAccessRight(request):
    '''
    必然来自授权
    '''
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    aPhone = User.objects.get(phone=request.GET['aPhone'])
    ud = UserDevice(deviceId=device,phone=phone,source=2,aPhone=aPhone)
    ud.save()
    return HttpResponse(json.dumps({
        'res':True,
        'deviceRight':getDeviceRight(phone.phone, ud),
        'deviceConfig':getDeviceConfig(device,ud)
        }),content_type="application/json")

## addCtrlRight|deviceId,phone,source[,aPhone]|deviceConfig,deviceRight
def addCtrlRight(request):
    '''
    输入密码获得
    授权获得
    '''
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    aPhone = User.objects.get(phone=request.GET['aPhone'])
    ud = 'init'
    if not UserDevice.objects.filter(deviceId=device,phone=phone).exists():
        ud = UserDevice(deviceId=device,phone=phone)
    else:
        ud = UserDevice.objects.get(deviceId=device,phone=phone)
    ud.source = int(request.GET['source'])
    if ud.source == 3: # 来自密码
        ud.pAccess = 1
    elif ud.source == 2: # 来自授权
        ud.aAccess = 1
        ud.aPhone = aPhone
    ud.save()
    return HttpResponse(json.dumps({
        'res':True,
        'deviceRight':getDeviceRight(phone.phone, ud),
        'deviceConfig':getDeviceConfig(device,ud)
        }),content_type="application/json")


## delRight|deviceId,phone|res
def delRight(request):
    device = Device.objects.get(deviceId=request.GET['deviceId'])
    phone = User.objects.get(phone=request.GET['phone'])
    UserDevice.objects.filter(deviceId=device,phone=phone).delete()
    return HttpResponse(json.dumps({
        'res':True
        }),content_type="application/json")

