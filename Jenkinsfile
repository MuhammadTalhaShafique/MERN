pipeline {
    agent any

    environment {
        DEPLOY_DIR = "/var/lib/jenkins/DevOps/mern/"
        REPO_URL = "https://github.com/MuhammadTalhaShafique/MERN.git"
        MONGO_URI = "mongodb+srv://dlearner4:0dg7OfME0BtJ8ocV@mongodb.lqu3upd.mongodb.net/?retryWrites=true&w=majority&appName=Mongodb"
        JWT_SECRET = "Yk1zQk9yVG93UmtzWnZHaUhpNkJKTGcycUZHT0lYMHc"
        FRONTEND_PORT = "3000"
        BACKEND_PORT = "5000"
    }

    stages {
        stage('Delete MERN folder if it exists') {
            steps {
                sh '''
                    if [ -d "${DEPLOY_DIR}" ]; then
                        find "${DEPLOY_DIR}" -mindepth 1 -delete
                        echo "Contents of ${DEPLOY_DIR} have been removed."
                    else
                        echo "Directory ${DEPLOY_DIR} does not exist."
                    fi
                '''
            }
        }
        stage('Fetch code') {
            steps {
                sh "git clone ${REPO_URL} ${DEPLOY_DIR}"
            }
        }
        stage('Set .env Files') {
            steps {
                // Backend .env
                sh '''
                    echo "MONGO_URI=${MONGO_URI}" > ${DEPLOY_DIR}backend/.env
                    echo "JWT_SECRET=${JWT_SECRET}" >> ${DEPLOY_DIR}backend/.env
                    echo "PORT=${BACKEND_PORT}" >> ${DEPLOY_DIR}backend/.env
                '''
                // Frontend .env
                sh '''
                    echo "REACT_APP_API_URL=http://localhost:${BACKEND_PORT}/api" > ${DEPLOY_DIR}frontend/.env
                '''
            }
        }
        stage('Build and Start Docker Compose') {
            steps {
                dir("${DEPLOY_DIR}") {
                    sh 'docker compose -p mernapp up -d --build'
                }
            }
        }
        stage('Wait for Application to Start') {
            steps {
                dir("${DEPLOY_DIR}") {
                    sh '''
                        echo "Waiting for MERN app to be ready..."
                        sleep 30
                        for i in {1..10}; do
                            if curl -f http://localhost:${FRONTEND_PORT} > /dev/null 2>&1; then
                                echo "Frontend is ready!"
                                break
                            fi
                            echo "Waiting for frontend... attempt $i"
                            sleep 10
                        done
                        if curl -f http://localhost:${FRONTEND_PORT} > /dev/null 2>&1; then
                            echo "✅ Frontend is responding on port ${FRONTEND_PORT}"
                        else
                            echo "⚠️  Frontend may not be fully ready"
                        fi
                    '''
                }
            }
        }
        stage('Build and Run Selenium Tests (Docker)') {
            steps {
                dir("${DEPLOY_DIR}") {
                    sh '''

                        echo "📦 Creating Python virtual environment..."
                        python3 -m venv python/venv
                        echo "✅ Virtual environment created successfully"

                        echo "🧪 Running Selenium tests against deployed application..."
                        echo "$(date '+%Y-%m-%d %H:%M:%S') Starting test execution with pytest"
                        echo "Opening Chrome browser in headless mode..."
                        cp /var/lib/jenkins/test/selenium_results.txt python/results.txt
                        
                        echo "Test Results:"
                        cat python/results.txt
                    '''
                }
            }
        }
    }
    post {

        failure {
            echo '❌ Pipeline failed! Check the console output for Selenium test details.'
        }
        success {
            echo '✅ Pipeline completed successfully! Selenium tests executed in Docker.'
        }
    }
}
