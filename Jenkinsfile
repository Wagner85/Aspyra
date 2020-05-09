pipeline {
  agent any
  stages {
    stage('ping') {
      parallel {
        stage('ping') {
          steps {
            bat(script: 'ping 8.8.8.8 ', returnStatus: true)
          }
        }

        stage('ping 2') {
          steps {
            bat(script: 'ping google.com.br ', returnStatus: true)
          }
        }

        stage('ping 3') {
          steps {
            bat(script: 'ping stone.com.br', returnStatus: true)
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