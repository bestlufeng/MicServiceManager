# MicServiceManager
微服务管理&amp;部署工具






实现方式:jenkins调用MSM-api拉取微服务配置，实现流水线构建部署，MSM调用kubernetes api实现configmap service deployment的更新部署

jenkins  <====> MSM  <=====> kubernetes api


