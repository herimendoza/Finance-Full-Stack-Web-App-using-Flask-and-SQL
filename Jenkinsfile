pipeline {
  agent any
   stages {
    stage ('Build') {
      steps {
        sh '''#!/bin/bash
        python3 -m venv test1
        source test1/bin/activate
        pip install pip --upgrade
        pip freeze > requirements.txt
        pip install -r requirements.txt
        export FLASK_APP=application
        flask run --host=0.0.0.0 &
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