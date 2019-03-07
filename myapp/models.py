# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# 服务
class Service(models.Model):
    name = models.CharField(null=False,max_length=32)
    Mark = models.CharField(null=True,max_length=64)

# 微服务
class MicService(models.Model):
    name = models.CharField(null=False,max_length=32,unique=True)
    Service = models.ForeignKey(to=Service)
    # 容器部署相关配置
    limits_cpu = models.IntegerField(default=1000,null=False)
    limits_mem = models.IntegerField(default=2000,null=False)
    requests_cpu = models.IntegerField(default=500,null=False)
    requests_men = models.IntegerField(default=1000,null=False)
    port = models.IntegerField(default=8080,null=False)
    image = models.CharField(default="docker-hub.tools.huawei.com/clouddragon/euler",null=False,max_length=128)
    replicas = models.IntegerField()
# 环境
class Env(models.Model):
    name = models.CharField(null=False,max_length=32)
    mark = models.CharField(null=True,max_length=64)

# 镜像tag表
class Tags(models.Model):
    tag = models.CharField(null=False,max_length=32)
    mark = models.CharField(max_length=64,null=True)
    MicService = models.ForeignKey(to=MicService)