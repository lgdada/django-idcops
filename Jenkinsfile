pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''
        mkdir -p /home/mysite && cd /home/mysite
        '''
      }
    }
    post {
      always {
            junit 'build/reports/**/*.xml'
        }
    }
  }
}
