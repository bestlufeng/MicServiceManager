FROM docker-hub.alpha.tools.huawei.com/lufeng/django-nginx:1.0
# 更新基础镜像
ENV APP_NAME msm
RUN mkdir -p /usr/local/${APP_NAME}
WORKDIR /usr/local/${APP_NAME}
COPY ./requirements.txt ./requirements.txt
RUN yum install -y gcc python-devel \
   && pip install -r ./requirements.txt
ENV TZ 'Asia/Shanghai'
COPY . ./
EXPOSE 8080
CMD ["/bin/bash", "./runserver.sh"]
