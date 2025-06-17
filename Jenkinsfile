pipeline {
    agent any

    environment {
        EC2_HOST = '13.48.163.120' // TODO: Your EC2 public IP
        EC2_USER = 'ubuntu'        // TODO: Your EC2 username
        PROJECT_DIR = '/home/ubuntu/your-app-folder' // TODO: Path on EC2
        // The following assumes your Jenkins node has SSH keys set up for passwordless login to EC2
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Deploy on EC2') {
            steps {
                script {
                    // Copy repo to EC2
                    sh """
                      ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'rm -rf ${PROJECT_DIR}'
                      scp -o StrictHostKeyChecking=no -r . ${EC2_USER}@${EC2_HOST}:${PROJECT_DIR}
                    """
                    // Build and deploy with Docker Compose on EC2
                    sh """
                      ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                        cd ${PROJECT_DIR} &&
                        docker-compose down || true &&
                        docker-compose up -d --build
                      '
                    """
                }
            }
        }
        stage('Run Selenium Tests on EC2') {
            steps {
                script {
                    // Run selenium tests inside EC2 using Docker (pytest output redirected to results.txt)
                    sh """
                      ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                        cd ${PROJECT_DIR}/selenium-tests &&
                        docker build -t selenium-tests . &&
                        docker run --rm selenium-tests > results.txt || true
                      '
                      scp -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST}:${PROJECT_DIR}/selenium-tests/results.txt .
                    """
                }
            }
        }
        stage('Email Test Results to Committer') {
            steps {
                script {
                    // Get committer's email from the latest commit
                    def committerEmail = sh(
                        script: "git log -1 --pretty=format:'%ae'",
                        returnStdout: true
                    ).trim()
                    def testResults = readFile 'results.txt'

                    emailext (
                        to: committerEmail,
                        subject: "Selenium Test Results for your commit",
                        body: """Hello,

Here are the Selenium test results for your recent commit:

${testResults}

Regards,
Jenkins CI/CD
"""
                    )
                }
            }
        }
    }
}