# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import models
import time,datetime,json
import requests
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

# Create your views here.
# 主页跳转到前端页面
def index(request):
    return HttpResponseRedirect('/static/index.html')

# 健康检查地址
def health_check(request):
    return HttpResponse("true")

# 后期更改的默认值
namespace = "msm"
# kube_server = "http://100.101.93.72:8080"
kube_server = "https://192.168.1.6:82/k8s/clusters/c-vmmmm"
kube_headers = {}


# 定义response 标准格式
std_use_response = {
    "result": True,
    "data": "",
    "message": ""
}

def mic_service(request):
    std_response = {
        "result": True,
        "data": "",
        "message": ""
    }
    MicServiceId = request.GET.get("MicServiceId")
    def get_data():
        MicService = list(models.MicService.objects.filter(id=MicServiceId).values("limits_cpu",
        "name",
        "replicas",
        "image",
        "port",
        "requests_cpu",
        "requests_men",
        "limits_mem",
        "Service__name",
        "Service_id",
        "id",))[0]
        return MicService
    if request.method == "GET":
        try:
            MicService = get_data()
            std_response["data"] = MicService
        except Exception as e:
            std_response["message"] = str(e)
            std_response["result"] = False
        return HttpResponse(json.dumps(std_response))
    if request.method == "PUT":
        try:
            info = json.loads(request.body)
            models.MicService.objects.filter(id=MicServiceId).update(**info)
            MicService = get_data()
            std_response["data"] = MicService
        except Exception as e:
            std_response["message"] = str(e)
            std_response["result"] = False
        return HttpResponse(json.dumps(std_response))
    if request.method == "POST":
        info = json.loads(request.body)
        try:
            models.MicService.objects.create(**info)
            std_response["message"] = "service add successful"
        except Exception as e:
            print e
            std_response["result"] = False
            std_response["error"] = str(e)
        return HttpResponse(json.dumps(std_response))

def jenkins_file(request):
    info = {
        "name" : "app01",
        "MicServiceId" : 1,
        "image" : "docker.io/jenkins/jenkins",
        "smsAddr" : "127.0.0.1"
    }
    return render(request,"Jenkinsfile",{
        "info": info
    })

# 获取服务树
def service(request):
    std_response = {
        "result": True,
        "data": "",
        "message": ""
    }
    services = list(models.Service.objects.all().values())
    mic_services = list(models.MicService.objects.all().values())
    # for mic_service in mic_services:
    #     for service in services:
    #         if mic_service["Service_id"] == service["id"]:
    #             services
    std_response["data"] = [
        {
            "name":"service1",
            "data":[
                {"name": "mic1"},
                {"name": "mic2"},
                {"name": "mic3"},
            ]
        },
        {
            "name":"service2",
            "data":[
                {"name": "mic4"},
                {"name": "mic5"},
                {"name": "mic6"},
            ]
        },
    ]
    return HttpResponse(json.dumps(std_response))


def kubenetes_deployment(request):
    MicServiceId = request.GET.get("MicServiceId")
    MicService = list(models.MicService.objects.filter(id=MicServiceId).values())[0]
    appName = MicService["name"]
    appEnv = request.GET.get("envId")
    replicas = MicService["replicas"]
    image = str(MicService["image"]+":"+"1.1.1")
    containerPort = MicService["port"]
    deployment =  {
        "apiVersion": "extensions/v1beta1",
        "kind": "Deployment",
        "metadata": {
            "name": str(appName),
            "namespace": str(namespace+"-"+appEnv),
            "labels": {
                "appname": appName,
                "appenv": appEnv
            }
        },
        "spec": {
            "replicas": int(replicas),
            "selector": {
                "matchLabels": {
                    "appname": appName,
                    "appenv": appEnv
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "appname": appName,
                        "appenv": appEnv
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": appName,
                            "image": image,
                            "ports": [
                                {
                                    "containerPort": int(containerPort)
                                }
                            ],
                            "livenessProbe":{
                                "tcpSocket":{
                                    "port": int(containerPort)
                                },
                                "initialDelaySeconds": 30,
                                "timeoutSeconds": 1
                            },
                            "imagePullPolicy": "Always",
                            "envFrom":[
                                {
                                    "configMapRef": {
                                        "name": str(appName),
                                    },
                                 }
                            ],
                            "env": [
                                {
                                    "name": "appname",
                                    "value": appName
                                },
                                {
                                    "name": "appenv",
                                    "value": appEnv
                                },
                                {
                                    "name": "mic_service_id",
                                    "value": MicServiceId
                                },
                                {
                                    "name": "deployTime",
                                    "value": str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((time.time()))))
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    if request.method == "GET":
        url = str(kube_server+"/apis/extensions/v1beta1/namespaces/"+ namespace+ "-" + appEnv  +"/deployments/" + appName)
        kube_data = requests.request(method=request.method,url=url,verify=False,headers=kube_headers)
        response = {
            "result" : True,
            "data": deployment,
            "kube_data": json.loads(kube_data.text),
            "message": None
        }
        return HttpResponse(json.dumps(response))
    if request.method == "POST":
        url = str(kube_server+"/apis/extensions/v1beta1/namespaces/"+ namespace+ "-" + appEnv  +"/deployments/")
        response = requests.request(method=request.method,url=url,verify=False,headers=kube_headers,data=json.dumps(deployment))
        return HttpResponse(response)
    if request.method == "PUT":
        url = str(kube_server+"/apis/extensions/v1beta1/namespaces/"+ namespace+ "-" + appEnv  +"/deployments/" + appName)
        response = requests.request(method=request.method,url=url,verify=False,headers=kube_headers,data=json.dumps(deployment))
        return HttpResponse(response)


def kubenetes_service(request):
    MicServiceId = request.GET.get("MicServiceId")
    MicService = list(models.MicService.objects.filter(id=MicServiceId).values())[0]
    appName = MicService["name"]
    appEnv = request.GET.get("envId")
    # replicas = MicService["replicas"]
    # image = str(MicService["image"]+":"+"1.0")
    containerPort = MicService["port"]
    service = {
      "kind": "Service",
      "apiVersion": "v1",
      "metadata": {
        "name": appName,
        "namespace": str(namespace+"-"+appEnv),
        "labels": {
          "appenv": appEnv,
          "appname": appName,
        }
      },
      "spec": {
        "ports": [
          {
            "protocol": "TCP",
            "port": int(containerPort),
            "targetPort": int(containerPort),
          }
        ],
        "selector": {
          "appenv": appEnv,
          "appname": appName,
        },
        "type": "NodePort",
      },
    }
    if request.method == "GET":
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/services/" + appName)
        kube_data = requests.request(method=request.method,url=url,verify=False,headers=kube_headers).text
        # print kube_data.text
        response = {
            "result" : True,
            "json_file": service,
            "kube_data" : json.loads(kube_data),
            "message": None
        }
        return HttpResponse(json.dumps(response))
    if request.method == "PUT":
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/services/" + appName)
        response_temp = json.loads(requests.request(method="GET",url=url,headers=kube_headers,data=json.dumps(service)).text)
        response_temp["spec"]["ports"][0]["port"] = MicService["port"]
        response_temp["spec"]["ports"][0]["targetPort"] = MicService["port"]
        response = requests.request(method="PUT",url=url,headers=kube_headers,data=json.dumps(response_temp))
        return HttpResponse(response)
    if request.method == "POST":
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/services/")
        response = requests.request(method=request.method,url=url,verify=False,headers=kube_headers,data=json.dumps(service))
        return HttpResponse(response)


# read_namespaced_config_map
def config_map(request):
    MicServiceId = request.GET.get("MicServiceId")
    MicService = list(models.MicService.objects.filter(id=MicServiceId).values())[0]
    appName = MicService["name"]
    appEnv = request.GET.get("envId")
    data = {
    "apiVersion": "v1",
    "data": {
        "mic_service_id": MicServiceId,
        "appname": appName,
        "appenv": appEnv,
    },
    "kind": "ConfigMap",
    "metadata": {
        "labels": {
            "appenv": appEnv,
            "appname": appName
        },
        "name": appName,
        # "namespace": str(namespace + appEnv)
        }
    }
    if request.method == 'POST':
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/configmaps/")
        response = requests.request(method="POST",url=url,verify=False,headers=kube_headers,data=json.dumps(data))
        return HttpResponse(response)
    if request.method == 'GET':
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/configmaps/" + appName)
        response = requests.request(method=request.method,url=url,verify=False,headers=kube_headers)
        return HttpResponse(response)
    if request.method == "PUT":
        url = str(kube_server+"/api/v1/namespaces/"+ namespace+ "-" + appEnv  +"/configmaps/" + appName)
        data["data"] = json.loads(request.body)
        print json.dumps(data)
        response = requests.request(method=request.method,url=url,headers=kube_headers,data=json.dumps(data))
        return HttpResponse(response)


