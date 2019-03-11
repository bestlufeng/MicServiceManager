# MicServiceManager
微服务管理&amp;部署工具



方式:jenkins调用sms-api拉取微服务配置，实现流水线构建部署，sms调用kubernetes api实现configmap service deployment的更新部署

jenkins  <====> sms  <=====> kubernetes api



调用kubernetes接口，配合Jenkins实现容器化的持续集成部署
