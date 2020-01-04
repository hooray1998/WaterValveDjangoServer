# -*- coding:utf-8 -*-

import requests
import json
import random

# host = '192.168.1.101:8000/'
host = 'http://0.0.0.0:8000/'

def createDevice(index):
    return {
        'name':'Name%d'%index,
        'serialNum':'nuaa_%d'%index,
        'remark':'备注%d'%index
        }
def createDevices():
    for index in range(1,10):
        r = requests.get(host+'registerDevice',params=createDevice(index))
        print(json.dumps(json.loads(r.text),indent=4))

def createUser(index):
    return {
            'phone':'phone_%d'%index,
            'openid':'openid_%d'%index
            }

def createUsers():
    for index in range(1,4):
        # print(host+'bindPhone',params=createUser(index))
        r = requests.get(host+'bindPhone',params=createUser(index))
        print(json.dumps(json.loads(r.text),indent=4))

def bindUserDevice():
    urls = []
    urls.append(host + 'addDevice?phone=phone_1&serialNum=nuaa_1&source=0')
    urls.append(host + 'addDevice?phone=phone_2&serialNum=nuaa_2&source=0')
    urls.append(host + 'addDevice?phone=phone_3&serialNum=nuaa_3&source=0')
    urls.append(host + 'addDevice?phone=phone_1&serialNum=nuaa_2&source=0')
    urls.append(host + 'addDevice?phone=phone_1&serialNum=nuaa_3&source=0')
    urls.append(host + 'addDevice?phone=phone_2&serialNum=nuaa_1&source=0')
    urls.append(host + 'addDevice?phone=phone_2&serialNum=nuaa_3&source=0')
    urls.append(host + 'addDevice?phone=phone_3&serialNum=nuaa_1&source=0')
    urls.append(host + 'addDevice?phone=phone_3&serialNum=nuaa_2&source=0')
    for url in urls:
        r = requests.get(url)
        print(json.dumps(json.loads(r.text)))

def init():
    createDevices()
    createUsers()
    bindUserDevice()

# init()
def check(func,**params):
    url = host + func + '?'
    r = requests.get(url, params=params)
    print(json.dumps(json.loads(r.text),indent=4))


## getOpenId        | code                           | openid
## bindPhone        | phone,openid                   | res
## addDevice        | phone,serialNum,source         | deviceList
## delDevice        | deviceId,phone                 | deviceList
## userDevices      | phone                          | deviceList
## userDeviceInfo   | deviceId,phone                 | deviceInfo
## userDeviceConfig | deviceId,phone                 | deviceConfig
## deviceInfoCtrl   | deviceId,phone,xxx             | deviceInfo/deviceConfig  | xxx=(remarkName|name|remark|position|ioState|accuracy)
## startAccessCtrl  | deviceId,phone                 | device
## updatePassword   | deviceId,password              | deviceConfig
## deviceLog        | deviceId,phone                 | log
## addAccessRight   | deviceId,phone,aPhone          | deviceConfig,deviceRight
## addCtrlRight     | deviceId,phone,source[,aPhone] | deviceConfig,deviceRight | source=2时增加aPhone
## delRight         | deviceId,phone                 | res

check('deviceLog', phone='phone_2', deviceId=1,source=2, aPhone='phone_1')
# check('addCtrlRight', phone='phone_2', deviceId=1,source=2, aPhone='phone_1')
# check('deviceInfoCtrl', phone='phone_2', deviceId=1, name='me')
# check('userDeviceInfo', phone='phone_2', deviceId=1)
# check('userDeviceConfig', phone='phone_2', deviceId=1)
# check('userDevices', phone='phone_3')
# check('delRight', phone='phone_2', deviceId=1)

# check('')
