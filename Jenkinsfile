
pipeline {
    agent any

    environment {
        APP_IMAGE = 'seleniumtestingdemoapp:latest'
        CONTAINER_NAME = 'seleniumtestingdemoapp-test'
        APP_URL = 'http://127.0.0.1:5000'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install Flask pytest selenium
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${APP_IMAGE} .'
            }
        }

        stage('Start Application') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} \
                        -p 5000:5000 ${APP_IMAGE}

                    for i in $(seq 1 30); do
                        if curl -fsS ${APP_URL}/register > /dev/null; then
                            echo "Application is ready"
                            exit 0
                        fi
                        sleep 2
                    done

                    docker logs ${CONTAINER_NAME}
                    exit 1
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh 'python3 -m pytest -v tests/test_registrationapp.py'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${CONTAINER_NAME} || true'
            junit testResults: 'test-results.xml',
                  allowEmptyResults: true
        }
    }
}
