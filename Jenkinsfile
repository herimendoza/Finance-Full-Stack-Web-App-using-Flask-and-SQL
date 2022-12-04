pipeline {
  agent any
   stages {
    stage ('Build') {
      steps {
        sh '''#!/bin/bash
        python3 -m venv financevenv
        source financevenv/bin/activate
        pip install pip --upgrade
        pip freeze > requirements.txt
        pip install -r requirements.txt
        export FLASK_APP=application
        flask run &
        '''
     }
   }
    // stage ('test') {
    //   steps {
    //     sh '''#!/bin/bash
    //     source test3/bin/activate
    //     py.test --verbose --junit-xml test-reports/results.xml
    //     ''' 
    //   }
    
    //   post{
    //     always {
    //       junit 'test-reports/results.xml'
    //     }
       
    //   }
    // }
  }
 }