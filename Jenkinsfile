pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh '''#!/bin/bash
pwd
ls -l
old_id=`docker images ${image} -q`
docker build -t ${image} -f ./dockerfile .
new_id=`docker images ${image} -q`
if [ ${old_id} != ${new_id} ];then
	docker rmi ${old_id}
fi 
docker push ${image}'''
      }
    }
    stage('deploy') {
      parallel {
        stage('alpha') {
          steps {
            input 'is depoy alpha'
            echo 'begin to deploy alpha'
            sh '''#!/bin/bash
echo 'update configmap'
python ./deploy_to_k8s.py configmap | python -m json.tool
python ./deploy_to_k8s.py configmap | kubectl apply -f - --record
echo 'update service'
python ./deploy_to_k8s.py service | python -m json.tool
python ./deploy_to_k8s.py service | kubectl apply -f - --record
echo 'update deployment'
python ./deploy_to_k8s.py deployment | python -m json.tool
python ./deploy_to_k8s.py deployment | kubectl apply -f - --record
'''
          }
        }
        stage('beta') {
          steps {
            echo 'start to deploy beta'
            input 'is deploy beta'
          }
        }
      }
    }
  }
  environment {
    appName = 'msm'
    appEnv = 'alpha'
    replicas = '2'
    image = 'docker-hub.alpha.tools.huawei.com/lufeng/django-app:1.0.2'
    containerPort = '8080'
    containerEnv = '[{"name": "DEBUG", "value": "False"}, {"name": "myid", "value": "14313131"}]'
  }
}
