#!/bin/bash
# supervisord -c ./supervisord.conf
# supervisorctl start all
# /usr/local/bin/python /usr/local/bin/supervisord -c ./supervisord.conf
# 添加定时任务
#python manage.py crontab add
# 启动定时任务服务
/usr/sbin/crond
# 配置及启动nginx
mv ./nginx.conf /etc/nginx/conf.d/app.conf && nginx
# 启动django服务
uwsgi --ini ./uwsgi.ini
