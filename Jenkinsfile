pipeline {
    agent {
        label 'KZ01_TI-141_OZP_CentOS'
    }
    stages {
        stage('Checkout Repo') {
            steps {
                git url: 'http://www.github.com/mark-betters-ozp-forks/ozp-backend.git', branch: 'master'
            }
        }
        stage('Make Python Environment') {
            steps {
                sh 'mkdir -p python-env'
                sh 'sudo /usr/local/bin/pyvenv-3.4 python-env'
            }
        }
        stage('Install PIP') {
            steps {
                sh '. ./python-env/bin/activate'
                sh 'wget https://bootstrap.pypa.io/get-pip.py'
                sh 'sudo python get-pip.py'
            }
        }
        stage('Install Backend Dependencies') {
            steps {
                sh '. ./python-env/bin/activate'
                sh 'pip install --upgrade pip'
                sh 'pip install wheel'
                sh 'export PATH=/usr/local/pgsql/bin:$PATH'
                sh 'pip install -e "git+https://github.com/nssbu/django-cas.git#egg=django-cas-client-ozp"'
                sh 'pip install --no-cache-dir -I -r requirements.txt'
                sh 'ldd python-env/lib/python3.4/site-packages/PIL/_imaging.cpython-34m.so'
            }
        }
        stage('Build the Release Tarball') {
            steps {
                sh '. ./python-env/bin/activate'
                sh 'export PATH=/usr/local/pgsql/bin:$PATH'
                sh 'python release.py --no-version'
                sh 'mv *.tar.gz backend.tar.gz'
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