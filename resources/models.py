from django.db import models

# Create your models here.


class Idc(models.Model):
    name = models.CharField(max_length=10, verbose_name='机房简称', unique=True)
    name_cn = models.CharField(max_length=32, verbose_name='机房中文名')
    address = models.CharField(max_length=64, null=True, blank=True, verbose_name='机房地址，云厂商可以不写')
    username = models.CharField(max_length=32, verbose_name='机房负责人')
    username_phone = models.CharField(max_length=32, verbose_name='机房负责人联系电话')
    phone = models.CharField(max_length=32, verbose_name='机房电话')
    email = models.EmailField(verbose_name='机房邮箱')

    class Meta:
        db_table = 'resources_idc'


class ServerAuto(models.Model):
    ip_inner = models.CharField(max_length=32, verbose_name='连接IP地址')
    port = models.IntegerField(verbose_name='连接端口')
    os_status_list = [
        (0, 'Linux'),
        (1, 'Windows'),
        (2, 'Mac')
    ]
    os_status = models.IntegerField(choices=os_status_list,verbose_name='操作系统')
    system_status_list = [
        (0, '虚拟机'),
        (1, '物理机'),
        (2, '虚拟化')
    ]
    system_status = models.IntegerField(choices=system_status_list, verbose_name='机器类型')


class Server(models.Model):
    hostname = models.CharField(max_length=64, verbose_name='主机名')
    cpu_info = models.CharField(max_length=64, verbose_name='CPU型号')
    cpu_count = models.IntegerField(verbose_name='CPU物理个数')
    mem_info = models.CharField(max_length=32, verbose_name='内存信息')
    disk_info = models.CharField(max_length=64, verbose_name='硬盘信息')
    ip_info = models.CharField(max_length=64, verbose_name='IP信息')
    os_system = models.CharField(max_length=32, verbose_name='系统平台')
    os_system_num = models.IntegerField(verbose_name='系统平台位数')
    uuid = models.CharField(max_length=64, verbose_name='UUID')
    sn = models.CharField(max_length=64, verbose_name='SN')
    scan_status_list = [
        (0, '连接异常'),
        (1, '连接正常')
    ]
    scan_status = models.IntegerField(choices=scan_status_list, verbose_name='探测状态')
    info = models.CharField(max_length=64, verbose_name='备注')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建主机时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新主机时间')
    server_auto = models.OneToOneField('ServerAuto')