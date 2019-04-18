from __future__ import print_function
from jenkinsapi.jenkins import Jenkins
# from django.settings import JenkinsInfo
import sys
import time
import xmltodict

# jenkins api
reload(sys)
sys.setdefaultencoding('utf8')
jenkins_url = 'http://192.168.1.6:8080'
jenkins_user = 'jenkins'
jenkins_password = 'jenkins'

jenkins_instance = Jenkins(jenkins_url,jenkins_user,jenkins_password)
def jenkins_job(job_name,template_job,type):
    copy_job_name = template_job
    # print dir(jenkins_instance)
    xml = jenkins_instance[copy_job_name].get_config()
    if type == 'create':
        job = jenkins_instance.create_job(job_name, xml)
    elif type == 'update':
        job = jenkins_instance[job_name].update_config(xml)
    elif type == 'delete':
        job = jenkins_instance.delete_job(job_name)
    elif type == 'has_job':
        job = jenkins_instance.has_job(job_name)
    elif type == 'get_config':
        return xml
    else:
        pass
    return job

# def render_pipeline(template_job):

# get tag from harbor
def harbor():
    