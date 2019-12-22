from django.contrib import admin


from .models import User, Device, UserDevice
#导入需要管理的数据库表

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone','open_id','img')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-phone',)
    #后台数据列表排序方式
    list_display_links = ('phone', 'open_id')
    # 设置哪些字段可以点击进入编辑界面



@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_num',)

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'phone')
