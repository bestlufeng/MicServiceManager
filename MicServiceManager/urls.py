# -*- coding: utf-8 -*-
"""MicServiceManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from myapp import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^v1/health_check',views.health_check),
    
    url(r'^v1/kubenetes_deployment',views.kubenetes_deployment), # deployment接口
    url(r'^v1/kubenetes_service',views.kubenetes_service), # service接口
    url(r'^v1/config_map',views.config_map), # configmap 接口

    # 数据库交互接口
    url(r'^v1/services/mic_service$',views.mic_service),  # 微服务接口
    url(r'^v1/service$',views.service),  # 微服务接口
    url(r'^v1/env/(?P<envId>\d+)$',views.env),  # 单个环境环境
    url(r'^v1/envs$',views.envs),  # 所有环境接口
    url(r'^v1/env_config_params/(?P<envId>\d+)$',views.env_config_params),  # 获取环境配置 键值对
    url(r'^v1/micservice_config_params/mic_service/(?P<micServiceId>\d)/env/(?P<envId>\d+)$',views.micservice_config_params),  # 微服务环境配置 键值对
    # url(r'^v1/service',views.service),

    #jenkins 相关接口
    url(r'^v1/jenkins_file/mic_service/(?P<micServiceId>\d)/env/(?P<envId>\d+)$',views.jenkins_file),  # 微服务环境配置 键值对
    url(r'^v1/pipeline/mic_service/(?P<micServiceId>\d)/env/(?P<envId>\d+)',views.pipeline),  # 微服务环境配置 键值对
    #k8s相关接口



]