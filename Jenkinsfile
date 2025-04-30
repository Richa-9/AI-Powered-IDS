pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "ai_ids"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh 'docker-compose down || true'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Check Running Services') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo "Cleaning up dangling images (optional)"
            sh 'docker image prune -f || true'
        }
        failure {
            echo "Build failed! Check logs for details."
        }
    }
}
