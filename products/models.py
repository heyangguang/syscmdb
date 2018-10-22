from django.db import models

# Create your models here.


# 业务线模型
class Product(models.Model):
    name = models.CharField("业务线的名字", max_length=32)
    name_cn = models.CharField("业务线字母简称", max_length=10, db_index=True)
    op_interface = models.CharField(max_length=150, verbose_name='运维对接人')
    dev_interface = models.CharField(max_length=150, verbose_name='业务对接人')
    level = models.IntegerField(verbose_name='层级')
    pid = models.IntegerField("上级业务线ID", db_index=True)

    def __str__(self):
        return self.name_cn

    class Meta:
        default_permissions = []
        permissions = (
            ('add_product', '添加业务线'),
            ('delete_product', '删除业务线'),
            ('view_product', '查看业务线'),
            ('modify_product', '修改业务线'),
            ('add_product_host', '资产项目创建机器组'),
        )