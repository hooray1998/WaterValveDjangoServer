"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from blog import views
# 导入静态文件模块
from django.views.static import serve
# 导入配置文件里的文件上传配置
from django.conf import settings

# TODO: 理解这些URL的规则
urlpatterns = [
    #path('admin/', admin.site.urls)
    path('registerDevice', views.registerDevice), 
    path('getOpenId', views.getOpenId), 
    path('bindPhone', views.bindPhone), 
    path('addDevice', views.addDevice), 
    path('delDevice', views.delDevice), 
    path('userDevices', views.userDevices), 
    path('userDeviceInfo', views.userDeviceInfo), 
    path('userDeviceConfig', views.userDeviceConfig), 
    path('deviceInfoCtrl', views.deviceInfoCtrl),
    path('startAccessCtrl', views.startAccessCtrl),
    path('updatePassword', views.updatePassword),
    path('deviceLog', views.deviceLog),
    path('addAccessRight', views.addAccessRight),
    path('addCtrlRight', views.addCtrlRight),
    path('delRight', views.delRight) 

## getOpenId        | code                           | openid
## bindPhone        | openid,phone                   | res
## addDevice        | phone,serialNum,source         | deviceList
## delDevice        | phone,deviceId                 | deviceList
## userDevices      | phone                          | deviceList
## userDeviceInfo   | deviceId                       | deviceInfo
## userDeviceConfig | deviceId                       | deviceConfig
## deviceInfoCtrl   | deviceId,phone,xxx             | deviceInfo/deviceConfig  | xxx=(remarkName|name|remark|position|ioState|accuracy)
## startAccessCtrl  | deviceId                       | device
## updatePassword   | deviceId,password              | deviceConfig
## deviceLog        | deviceId                       | log
## addAccessRight   | deviceId,phone,aPhone          | deviceConfig,deviceRight
## addCtrlRight     | deviceId,phone,source[,aPhone] | deviceConfig,deviceRight | source=2时增加aPhone
## delRight         | deviceId,phone                 | res

# /getOpenId                | 获得openid   | (code)->(openid)->(res)
# /bindPhone                | 绑定手机     | (openid,phone)->(res)
# /addDevice                | 添加设备     | (phone,serialNum,source)->(res, deviceList)
# /delDevice                | 删除设备     | (phone,deviceId)->(res, deviceList)
# /userDevices              | 用户设备列表 | (phone)->(deviceList)
# /userDevice               | 单个设备信息 | (phone,deviceId)->(deviceInfo)
# /openDeviceCtrl           | 阀门开关控制 |(phone,deviceId,number)->(res,deviceInfo)
# /openDegree           | 阀门开度控制 | (phone,deviceId,number)->(res,deviceInfo)
# /setCtrlType              | 控制方式     |(phone,deviceId,number)->(res,deviceInfo)
# /setAccuracy              | 控制精度     |(phone,deviceId,number)->(res,deviceInfo)
# /getAccessCtrl            | 获取控制权限 |
# /userHistoryInfo          | 运行记录     |
# /updateDeviceName         | 修改设备名称 |
# /startAccessCtrl          | 启用控制权限 |
# /updateAccessCtrlPassword | 修改控制密码 |
# /getAccessCtrlUsers       | 获取用户权限 |
# /delAccessCtrlUsers       | 删除用户权限 |
# /addAccessCtrlUsers       | 添加用户权限 |


    # path('list-<int:lid>.html', views.list, name='list'), # 列表页; 传入一个整型参数lid
    # path('show-<int:sid>.html', views.show, name='show'), # 内容页; 传入一个整型参数sid
    # path('tag/<tag>', views.tag, name='tag'), # 标签列表页
    # path('s/', views.search, name='search'), # 搜索页
    # path('about', views.about, name='about'), # 联系我们页
    # path('author.html', views.author, name='author'), # 联系我们页
    # path('category', views.categoryPage, name='category'), # 联系我们页
    # path('book', views.book, name='book'), # 联系我们页
    # path('link', views.link, name='link'), # 联系我们页
    # path('test', views.test, name='test'), # 联系我们页

    # re_path(r'^search-form$', views.search_form),
    # re_path(r'^search$', views.search),

    # re_path(r'^search-post$', views.search_post),
    # re_path(r'^search-post3$', views.search_post3),
    ## path('comments/', include('django_comments.urls')), # 评论功能

    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),    # 使media中的图片正常显示
    ]

