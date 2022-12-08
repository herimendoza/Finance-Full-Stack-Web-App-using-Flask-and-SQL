pipeline {
  agent any
   stages {
    stage ('Build') {
      steps {
        sh '''#!/bin/bash
        python3 -m venv test1
        source test1/bin/activate
        pip install pip --upgrade
        pip install -r requirements.txt
        export FLASK_APP=application
        flask run &
        '''
     }
   }
   /*
    stage ('test') {
      steps {
        sh '''#!/bin/bash
        source test3/bin/activate
        py.test --verbose --junit-xml test-reports/results.xml
        ''' 
      }
    
      post{
        always {
          junit 'test-reports/results.xml'
        }
       
      }
    }
    stage ('e2e tests - cypress') {
      steps {

      }
    }

    stage ('Create Image') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }

    stage ('Push to Dockerhub') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }

    stage ('TF-init') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }

    stage ('TF-plan') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }

    stage ('TF-apply') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }

    stage ('TF-destroy') {
      agent{label 'REPLACE_LABEL'}
      steps {

      }
    }
    */

    
  }
  /*
  post{
    always{
      emailext to: <email>
    }
  }
  */
 }