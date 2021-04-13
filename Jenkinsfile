pipeline {
  agent any
  stages {
    stage('ping') {
      parallel {
        stage('ping') {
          steps {
            sh(script: 'ping 8.8.8.8 -c3 ', returnStatus: true)
          }
        }

        stage('ping 2') {
          steps {
            sh(script: 'ping google.com.br -c4  ', returnStatus: true)
          }
        }

        stage('ping 3') {
          steps {
            sh(script: 'ping stone.com.br -c4 ' , returnStatus: true)
          }
        }

      }
    }

    stage('teste2') {
      steps {
        echo 'echo teste 2 ok'
      }
    }

  }
}
