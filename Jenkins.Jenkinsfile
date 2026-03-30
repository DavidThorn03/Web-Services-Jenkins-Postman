pipeline {
    agent any
    stages {
        stage('clone') {
            steps {
                echo 'Get code from github repo'
                bat 'dir'
                checkout scmGit(branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/DavidThorn03/Web-Services-Jenkins-Postman.git']])
                bat 'dir'
            }
        }
        stage('Install Depenancies'){
            steps {
                echo 'Installing dependancies'
                bat 'pip install -r requirements.txt'
                bat 'npm install -g newman'
            }
        }
        stage('Create Env'){
            steps {
                echo 'Create env file'
                withCredentials([file(credentialsId: 'fastapi_env', variable: 'ENV_FILE')]) {
                    bat 'copy %ENV_FILE% .env'
                }
            }
        }
        stage('Build docker'){
            steps {
                echo 'Set up docker with code from git'
                bat 'docker build -t app .'
            }
        }
        stage('Run Container'){
            steps {
                echo 'Run docker container'
                bat 'docker run -d --name app -p 8000:8000 --env-file .env app'
            }
        }
        stage('Run tests') {
            steps {
                echo 'Now time to try test the code..'
                bat 'npx newman run Products.postman_collection.json --reporters cli,junit --reporter-junit-export results/newman-results.xml'
            }
            post {
                always {
                    junit 'results/newman-results.xml'
                }
            }
        }
        stage('Kill docker'){
            steps {
                echo 'Stop docker from running'
                bat 'docker stop app'
                bat 'docker rm app'
            }
        }
        stage('Create zip file'){
            steps {
                echo 'With api code and docker config from github'
                echo 'first delete old files'
                bat 'del complete_*.zip'
                bat "powershell Compress-Archive -Path main.py, Dockerfile -DestinationPath complete_${env.BUILD_TIMESTAMP}.zip"
            }
            post {
                success {
                    archiveArtifacts artifacts: 'complete_*.zip'
                }
            }
        }
    }
}