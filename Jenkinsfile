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

    stage ('Staging init') {
      agent{label 'terrage'}
      steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                        string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                            dir('Staging_Terra') {
                              sh 'terraform init' 
                            }
         }
      }
  }  
     stage('Staging Plan') {
      agent{label 'terrage'}   
      steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                        string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                            dir('Staging_Terra') {
                              sh 'terraform plan -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" -target=aws_vpc.finance-vpc -target=aws_instance.MySQL_Server -target=aws_subnet.subnet1 -target=aws_subnet.pri_subnet1 -target=aws_subnet.subnet2 -target=aws_subnet.pri_subnet2 -target=aws_internet_gateway.gw1 -target=aws_route_table.route_table1 -target=aws_route_table_association.route-subnet1 -target=aws_db_instance.financedb -target=aws_db_subnet_group.mysql_subnet_group' 
                            }
         }
    }
   }
     stage('Staging Apply') {
      agent{label 'terrage'}
      steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                        string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                            dir('Staging_Terra') {

                              sh 'terraform apply -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" -target=aws_vpc.finance-vpc -target=aws_instance.MySQL_Server -target=aws_subnet.subnet1 -target=aws_subnet.pri_subnet1 -target=aws_subnet.subnet2 -target=aws_subnet.pri_subnet2 -target=aws_internet_gateway.gw1 -target=aws_route_table.route_table1 -target=aws_route_table_association.route-subnet1 -target=aws_db_instance.financedb -target=aws_db_subnet_group.mysql_subnet_group' 
                            }
         }
       }
      }

     stage('Variables Add') {
       agent{label 'terrage'}
       steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'),
                        string(credentialsId: 'API_KEY', variable: 'API_KEY'), 
                        string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                        dir('Staging_Terra') {

                              sh '''#!/bin/bash
                              echo "API_KEY=${API_KEY}" >> output.txt
                              USER=$(terraform output -raw mysql_username)
                              PASSWORD=$(terraform output -raw mysql_password)
                              ENDPOINT=$(terraform output -raw mysql_host)
                              DATABASE=$(terraform output -raw mysql_database_name) 
                              DB_URI="mysql://${USER}:${PASSWORD}@${ENDPOINT}/${DATABASE}"
                              echo ${DB_URI}
                              echo "DB_URI=${DB_URI}" >> output.txt
                              '''
                            }         
      
       }
      }
     }      
   
     stage('Variables Apply') {
      agent{label 'terrage'}
      steps {
        withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                        string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                            dir('Staging_Terra') {

                              sh '''#!/bin/bash
                                  terraform plan -target=aws_instance.Web_Server -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" 
                                  terraform apply -target=aws_instance.Web_Server -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" 
                                  '''
                            }
         }
       }
      }

  
//   stage('Destroy') {
//       agent{label 'terrage'}
//       steps {
//         withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'),
//         string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
//         dir('Staging_Terra') {
//         sh 'terraform destroy -auto-approve -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key"'
//       }
//     }
//   }
//   }

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
