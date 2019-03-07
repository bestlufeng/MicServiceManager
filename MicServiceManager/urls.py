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
from django.conf.urls import url
from django.contrib import admin
from myapp import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^v1/health_check',views.health_check),
    url(r'^v1/kubenetes_deployment',views.kubenetes_deployment), # deployment接口
    url(r'^v1/kubenetes_service',views.kubenetes_service), # service接口
    url(r'^v1/config_map',views.config_map), # configmap 接口

    url(r'^v1/services/mic_service$',views.mic_service),  # 微服务接口
    url(r'^v1/service$',views.service),  # 微服务接口
    # url(r'^v1/service',views.service),
]