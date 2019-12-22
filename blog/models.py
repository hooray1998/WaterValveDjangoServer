from django.db import models

# 导入Django自带用户模块

# Create your models here.


# 用户数据表 user
# id				id			long
# 用户微信ID  	u_openid		var(40)
# 用户手机号		u_phone		var(20)
# 用户微信头像	u_img		var(50)
class User(models.Model):
    phone = models.CharField('手机号', max_length=20, primary_key=True)
    open_id = models.CharField('微信号', max_length=40,unique=True)
    img = models.CharField('微信头像', max_length=100, default='img_null')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.phone

# 推荐位
# id				id			long
# 设备编号		device_id		var(40)
# 日志类型		type			int
# 日志内容		log			var（100）
# 日志时间		time			datetime

# 日志类型：阀门访问，阀门控制，阀门参数设置，用户授权，控制密码修改等。
class DeviceLog(models.Model):
    log_type = models.IntegerField('日志类型')
    log_content = models.CharField('日志内容', max_length=100)
    created_time = models.DateTimeField('日志时间', auto_now_add=True)

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_id


# 设备信息表 device
# id				id			long
# 设备编号		device_id			var(40)
# 设备序列号		serial_num		var(40)
# 设备名称		name			var(40)
# 备注			remark			var(50)
# 访问控制启用	access_ctrl		int		（0代表未启用，1代表已经启用）
# 访问控制密码	c_pass			var(40)	 （默认为123456）
# 设备管理员账户	adm_phone		var(20)	 （默认为空）

class Device(models.Model):
    # 自动生成的作为device_id
    device_id = models.AutoField('设备标识', max_length=20, primary_key=True)
    serial_num = models.CharField('序列号', max_length=40,unique=True)
    name = models.CharField('设备名', max_length=40)
    remark = models.CharField('设备备注', max_length=50)

    access_ctrl = models.BooleanField('访问控制启用')
    c_pass = models.CharField('控制密码', max_length=20,default='123456')
    adm_phone = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='管理员账户', blank=True, null=True)


    position = models.IntegerField('设备开度',default=0)
    io_state = models.IntegerField('阀门开关量控制',default=0)
    accuracy = models.IntegerField('调节精度',default=0)
    state = models.IntegerField('阀门状态',default=0)
    network = models.IntegerField('网路连接',default=0)
    error = models.IntegerField('故障信息',default=0)

    log = models.ForeignKey(DeviceLog, on_delete=models.DO_NOTHING, verbose_name='系统日志', blank=True, null=True)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 用户设备 user_device
# id				id			long
# 用户账户		u_phone		var(20)
# 设备编号		device_id		var(40)
# 设备备注名称		remark_name			var(40)
# 访问来源		source		int		（0 代表扫码，1代表输入序列号，2被授权）
# 授权权限		a_access		int 		（0 代表仅访问， 1 代表访问+控制，默认0）
# 密码权限		p_access		int		（0 代表无密码，仅访问，1代表有密码，访问—+控制，默认为0）
# 授权者账户		a _phone		var(20)	
class UserDevice(models.Model):
    phone = models.ForeignKey(User,related_name='用户手机', on_delete=models.DO_NOTHING, verbose_name='用户手机号', blank=True, null=True)
    device_id = models.ForeignKey(Device, on_delete=models.DO_NOTHING, verbose_name='设备标识', blank=True, null=True)
    remark_name = models.CharField('设备备注', max_length=40)
    source = models.IntegerField('权限来源')
    a_access = models.IntegerField('a_access',default=0)
    p_access = models.IntegerField('p_access',default=0)
    a_phone = models.ForeignKey(User,related_name='授权用户手机号',  on_delete=models.DO_NOTHING, verbose_name='授权用户手机号', blank=True, null=True)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name
        unique_together=("phone","device_id")

    def __str__(self):
        return self.phone+self.device_id
