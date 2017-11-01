pipeline {
    agent {
        label 'KZ01_TI-141_OZP_CentOS'
    }
    environment {
        POSTGRES_VERSION = '9.5.9'
        PYTHON_VERSION = '3.4.3'
    }
    stages {
        stage('Checkout Repo') {
            steps {
                git url: 'http://www.github.com/mark-betters-ozp-forks/ozp-backend.git', branch: 'master'
            }
        }
        stage('Make Python Environment') {
            steps {
                sh '''
                  mkdir -p python-env
                  sudo /usr/local/bin/pyvenv-3.4 python-env
                '''
            }
        }
        stage('Install Backend Dependencies') {
            steps {
                sh '''
                  . ./python-env/bin/activate
                  sudo $(which pip) install --upgrade pip
                  sudo $(which pip) install wheel
                  export PATH=/usr/local/pgsql/bin:$PATH
                  sudo $(which pip) install -e "git+https://github.com/nssbu/django-cas.git#egg=django-cas-client-ozp"
                  sudo $(which pip) install --no-cache-dir -I -r requirements.txt
                  ldd python-env/lib/python3.4/site-packages/PIL/_imaging.cpython-34m.so
                '''
            }
        }
        stage('Build the Release Tarball') {
            steps {
                sh '''
                  . ./python-env/bin/activate
                  export PATH=/usr/local/pgsql/bin:$PATH
                  $(which python) release.py --no-version
                  mv backend-*.tar.gz backend.tar.gz
                '''
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'backend.tar.gz'
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished executing'
            echo 'Goodbye'
        }
    }
}