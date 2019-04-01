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
    gitlab_url = models.CharField(null=False,max_length=128)
    gitlab_dir = models.CharField(null=False,max_length=32) # 工程在代码中的路径


    # 容器部署相关配置
    docker_file_path = models.CharField(null=False,max_length=32)
    limits_cpu = models.IntegerField(default=1000,null=False)
    limits_mem = models.IntegerField(default=2000,null=False)
    requests_cpu = models.IntegerField(default=500,null=False)
    requests_men = models.IntegerField(default=1000,null=False)
    port = models.IntegerField(default=8080,null=False)
    health_check_type = models.CharField(null=False,max_length=32)  # port 端口检查 http 接口检查
    health_check_add = models.CharField(null=False,default='/',max_length=128) # 健康检查地址
    node_port = models.IntegerField(null=True)
    # image = models.CharField(default="docker-hub.tools.huawei.com/clouddragon/euler",null=False,max_length=128)
    replicas = models.IntegerField()

# 环境
class Env(models.Model):
    name = models.CharField(null=False,max_length=32)
    type = models.IntegerField(null=False) # 0代表测试环境 1代表生产环境 决定构建镜像的名称
    gitlab_branch = models.CharField(null=False,max_length=10) # 代码分支，同一环境所使用的代码分之保持一致
    deploy_paas = models.CharField(null=False,max_length=10) # 部署平台 kubernetes qixinPaaS
    deploy_type = models.CharField(null=False,max_length=10) # k8s
    kubernetes_api = models.CharField(null=False,max_length=128) # k8s api server地址
    kubernetes_token = models.CharField(null=False,max_length=128) # k8s api token
    kubernetes_namespace = models.CharField(null=False,max_length=10) # 命名空间 同一环境服务部署在k8s同一命名空间

    mark = models.CharField(null=True,max_length=64)


# 基于环境的配置参数
class EnvConfigParams(models.Model):
    Env = models.ForeignKey(to=Env)
    key = models.CharField(null=False,max_length=32)
    value = models.CharField(null=True,max_length=128)

# 基于服务和环境的配置参数
class MicServiceConfigParams(models.Model):
    MicService = models.ForeignKey(to=MicService)
    Env = models.ForeignKey(to=Env)
    key = models.CharField(null=False,max_length=32)
    value = models.CharField(null=True,max_length=128)

