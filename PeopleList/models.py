from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class People(models.Model):
    name = models.CharField(default='默认用户', max_length=50, verbose_name = '用户名')
    pid = models.IntegerField(default=1, verbose_name = '身份ID')
    department = models.CharField(default='某部门', max_length=50, verbose_name = '部门')
    classification = models.CharField(default='技术岗', max_length=50, verbose_name = '类别')
    rank = models.CharField(default='1级', max_length=50, verbose_name = '职级')
    tel = models.IntegerField(default=10086, verbose_name = '电话')#需要限制
    canteen = models.CharField(default='1号食堂', max_length=50, verbose_name = '食堂')

    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = '管理者')#上级管理者
    pub_date = models.DateTimeField(verbose_name = '创建时间')#创建时间

    def __str__(self):
        return self.name