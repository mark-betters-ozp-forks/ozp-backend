pipeline {
    agent {
        label 'KZ01_TI-141_OZP_CentOS'
    }
    environment {
        POSTGRES_VERSION = '9.5.9'
        PYTHON_VERSION = '3.4.3'
    }
    stages {
        stage('Install PostgreSQL If Not Installed') {
            steps {
                sh '''
                  if [ ! -f postgresql-${POSTGRES_VERSION}.tar.gz ]; then

                    # Ensure required packages are installed
                    sudo yum -y install readline-devel libtermcap-devel

                    # Download the PostgreSQL source
                    wget https://ftp.postgresql.org/pub/source/v${POSTGRES_VERSION}/postgresql-${POSTGRES_VERSION}.tar.gz

                    # Extract archive
                    tar -xzf postgresql-${POSTGRES_VERSION}.tar.gz

                    # Move into PostgreSQL dir
                    cd ${WORKSPACE}/postgresql-${POSTGRES_VERSION}

                    # Configure PostgreSQL
                    ./configure

                    # Make PostgreSQL
                    sudo make install
                    
                    #Install PostgreSQL Devel
                    sudo yum -y install postgresql-devel
        
                  fi
                '''
            }
        }
        stage('Install Python If Not Installed') {
            steps {
                sh '''
                  if [ ! -f Python-${PYTHON_VERSION}.tgz ]; then

                    # Download the Python source
                    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz

                    # Extract archive
                    tar -xzf Python-${PYTHON_VERSION}.tgz

                    # Move into python dir
                    cd ${WORKSPACE}/Python-${PYTHON_VERSION}

                    # Configure Python
                    ./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"

                    # Make python
                    make
                    sudo make altinstall
        
                  fi
                '''
            }
        }
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
                //TODO: Make backend.tar.gz into an artifact???
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