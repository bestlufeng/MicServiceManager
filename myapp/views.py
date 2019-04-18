# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import utils
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
# from utils import MyJenkinsApi
# from kubernetes import client, config
# from kubernetes.client.rest import ApiException
from pprint import pprint
import models
import time,datetime,json
import requests

# Create your views here.

# 定义response标准格式
def str_response(data,**kwargs):
    if kwargs.has_key("message"):
        str_message = kwargs["message"]
    else:
        str_message = ""
    if kwargs.has_key("result"):
        str_result = kwargs["result"]
    else:
        str_result = True
    response = {
        "result": str_result,
        "data": data,
        "message": str_message,
    }
    return json.dumps(response)

# 主页跳转到前端页面
def index(request):
    return HttpResponseRedirect('/static/index.html')

# 健康检查地址
def health_check(request):
    # return HttpResponse("true")
    a = {
        "result": True,
        "data": "yes"
    }
    return JsonResponse(a,safe=True)

# 后期更改的默认值
namespace = "msm"
# kube_server = "http://100.101.93.72:8080"
kube_server = "https://192.168.1.6:82/k8s/clusters/c-vmmmm"
kube_headers = {
        'Authorization': "Bearer kubeconfig-user-xrmxp:4wnwmzm4rqml6tnmd959bcmt9n9hj29llmwmb8xt47hg75xvzcpbvh",
}




def mic_service(request):
    std_response = {
        "result": True,
        "data": "",
        "message": ""
    }
    MicServiceId = request.GET.get("MicServiceId")
    def get_data():
        MicService = list(models.MicService.objects.filter(id=MicServiceId).values())[0]
        return MicService
    if request.method == "GET":
        try:
            MicService = get_data()
            return HttpResponse(str_response(data=MicService),content_type="application/json,charset=utf-8")
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
def env(request,**kwargs):
    envId = kwargs["envId"]
    if request.method == "GET":
        try:
            envInfo = list(models.Env.objects.filter(id=envId).values())[0]
            return HttpResponse(str_response(data=envInfo),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "PUT":
        post_data = json.loads(request.body)
        try:
            models.Env.objects.filter(id=envId).update(**post_data)
            envInfo = list(models.Env.objects.filter(id=envId).values())[0]
            return HttpResponse(str_response(data=envInfo),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "DELETE":
        try:
            models.Env.objects.filter(id=envId).delete()
            return HttpResponse(str_response(data="",message="delete successful"),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
def envs(request):
    if request.method == "GET":
        try:
            envs = list(models.Env.objects.all().values())
            return HttpResponse(str_response(data=envs),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "POST":
        post_data = json.loads(request.body)
        try:
            obj = models.Env.objects.create(**post_data)
            post_data["id"] = obj.id 
            return HttpResponse(str_response(data=post_data,message="add env successful"),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")

def env_config_params(request,**kwargs):
    envId = kwargs["envId"]
    if request.method == "GET":
        try:
            config_data = list(models.EnvConfigParams.objects.filter(Env_id=envId).values())
            return HttpResponse(str_response(data=config_data),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "POST":    
        try :
            post_data = json.loads(request.body)
            post_list = [ ]
            for param in post_data:
                param["Env_id"] = envId
                obj = models.EnvConfigParams(
                    **param
                )
                post_list.append(obj)
            models.EnvConfigParams.objects.bulk_create(post_list)
            return HttpResponse(str_response(data=post_data,message="post config params successful"),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "PUT":
        pass

def micservice_config_params(request,**kwargs):
    envId = kwargs["envId"]
    micServiceId = kwargs["micServiceId"]    
    if request.method == "GET":
        try:
            config_data = list(models.MicServiceConfigParams.objects.filter(Env_id=envId,MicService=micServiceId).values())        
            return HttpResponse(str_response(data=config_data),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")
    if request.method == "POST":    
        try :
            post_data = json.loads(request.body)
            post_list = [ ]
            for param in post_data:
                param["Env_id"] = envId
                param["MicService_id"] = micServiceId
                obj = models.MicServiceConfigParams(
                    **param
                )
                post_list.append(obj)
            models.MicServiceConfigParams.objects.bulk_create(post_list)
            return HttpResponse(str_response(data=post_data,message="post config params successful"),content_type="application/json,charset=utf-8")
        except Exception as e:
            result = False
            message = str(e)
            return HttpResponse(str_response(data="",message=message,result=result),content_type="application/json,charset=utf-8")

def jenkins_file(request,**kwargs):
    envId = kwargs["envId"]
    micServiceId = kwargs["micServiceId"]    
    if request.method == "GET":
        # try:
        envInfo = list(models.Env.objects.filter(id=envId).values())[0]
        micServiceInfo = list(models.MicService.objects.filter(id=micServiceId).values())[0]
        return render(request,"Jenkinsfile-chuangjiangx",{"data":{"envInfo":envInfo, "micServiceInfo":micServiceInfo}})

# def render_pipeline(request,**kwargs):
#     template_job = '111';
#     xml = utils.jenkins_job(job_name="0",template_job="test-pipeline")
    
#     return render(request,"")


def pipeline(request,**kwargs):
    envId = kwargs["envId"]
    micServiceId = kwargs["micServiceId"]
    envName = models.Env.objects.filter(id=envId).first().name
    micServiceName = models.MicService.objects.filter(id=micServiceId).first().name
    if request.method == "POST":   
        utils.jenkins_job(job_name=str(envName + "--" + micServiceName),template_job='111',type='create')
        message = 'create job successful'
    if request.method == "PUT":
        utils.jenkins_job(job_name=str(envName + "--" + micServiceName),template_job='111',type='update')
        message = 'update job successful'
    if request.method == "DELETE":
        utils.jenkins_job(job_name=str(envName + "--" + micServiceName),template_job='111',type='delete')
        message = 'delete job successful'
    if request.method == "GET":
        data = utils.jenkins_job(job_name=str(envName + "--" + micServiceName),template_job='111',type='has_job')
        message = 'query successful'
        return HttpResponse(str_response(data=data,message=message),content_type="application/json,charset=utf-8")
    return HttpResponse(str_response(data="",message=message),content_type="application/json,charset=utf-8")


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


