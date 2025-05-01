pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Richa-9/AI-Powered-IDS.git'
            }
        }

        stage('Build & Run Containers') {
            steps {
                bat 'docker-compose up -d'
            }
        }

        stage('Wait for Presentation') {
            steps {
                echo 'App is now running. Open it in your browser at http://localhost:3000 or http://localhost:5000'
                sleep(time:10, unit:"MINUTES") // You can change this to 5 or more
            }
        }

        stage('Shutdown App') {
            steps {
                bat 'docker-compose down'
            }
        }
    }
}
