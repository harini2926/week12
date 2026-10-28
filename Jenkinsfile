
pipeline {
    agent any

    environment {
        APP_IMAGE = 'seleniumtestingdemoapp:latest'
        CONTAINER_NAME = 'registrationapp'
        APP_URL = 'http://127.0.0.1:5000'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\Harini\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %APP_IMAGE% .'
            }
        }

        stage('Start Application') {
            steps {
                bat 'docker rm -f %CONTAINER_NAME% 2>NUL'
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %APP_IMAGE%'
                bat '''
                    powershell -NoProfile -Command "$ok=$false; for($i=0; $i -lt 30; $i++){ try { Invoke-WebRequest 'http://127.0.0.1:5000/register' -UseBasicParsing -TimeoutSec 2 | Out-Null; $ok=$true; break } catch { Start-Sleep -Seconds 2 } }; if(-not $ok){ docker logs registrationapp; exit 1 }"
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '"C:\\Users\\Harini\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest -v --junitxml=test-results.xml tests/test_registrationapp.py'
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results.xml',
                  allowEmptyResults: true
            bat 'docker rm -f registrationapp 2>NUL'
        }
    }
}
