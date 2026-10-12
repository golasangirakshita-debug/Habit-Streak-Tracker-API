pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Habit Streak Tracker source code'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '''
                    python3 -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t habit-streak-tracker:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                sh '''
                    docker image inspect habit-streak-tracker:${BUILD_NUMBER}
                '''

                echo 'Docker image built and verified successfully'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Pipeline completed successfully'
        }

        failure {
            echo 'FAILURE: Check the Jenkins console output'
        }

        always {
            echo 'Pipeline execution finished'
        }
    }
}