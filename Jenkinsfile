pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "ai_ids_project"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/Richa-9/AI-Powered-IDS.git', branch: 'main'
            }
        }

        stage('Build and Run with Docker Compose') {
            steps {
                script {
                    bat 'docker-compose down' // Clean before build
                    bat 'docker-compose build'
                    bat 'docker-compose up -d'
                }
            }
        }

        stage('Wait and Test') {
            steps {
                script {
                    echo 'Waiting for services to start...'
                    sleep 10
                    // Add any test commands here (like curl or healthcheck)
                }
            }
        }

        stage('Shutdown') {
            steps {
                bat 'docker-compose down'
            }
        }
    }
}
