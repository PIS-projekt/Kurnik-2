pipeline {
    agent any


    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup node and install frontend dependencies') {
            steps {
                dir('frontend') {
                    nodejs(nodeJSInstallationName: 'node-23') {
                        sh 'npm install'
                    }
                }
            }
        }

        stage('Lint frontend') {
            steps {
                dir('frontend') {
                    nodejs(nodeJSInstallationName: 'node-23') {
                        script {
                            echo 'Running ESLint...'
                            sh 'npm run lint'
                        }
                    }
                }
            }
        }

        stage('Run frontend tests') {
            steps {
                dir('frontend') {
                    nodejs(nodeJSInstallationName: 'node-23') {
                        script {
                            echo 'Running tests...'
                            sh 'npm run test'
                        }
                    }
                }
            }
        }

        stage('Build frontend') {
            steps {
                dir('frontend') {
                    nodejs(nodeJSInstallationName: 'node-23') {
                        script {
                            echo 'Building the project...'
                            sh 'npm run build'
                        }
                    }
                }
            }
        }


        stage('Build for Testing') {
            steps {
                script {
                    sh "docker build --target test -t backend-tests -f backend/Dockerfile backend/"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "docker run --rm backend-tests"
                }
            }
        }

        stage('Test Coverage') {
            steps {
                script {
                    sh "docker run --rm backend-tests pdm run coverage"
                }
            }
        }

        stage('Linting and Formatting') {
            steps {
                script {
                    // Adjust the linting/formatting tools as per your setup
                    sh "docker run --rm backend-tests pdm run lint"
                    sh "docker run --rm backend-tests pdm run format"
                }
            }
        }

        stage('Build for Production') {
            steps {
                script {
                    sh "docker stop prod_container && docker rm prod_container"
                    sh "docker build --target prod -t backend-prod -f backend/Dockerfile backend/"
                }
            }
        }

        stage('Verify Production Build') {
            steps {
                script {
                    // Verify the production build by running it temporarily
                    sh "docker run -p 8000:8000 -d --name prod_container backend-prod"

                    // Run a health check or test endpoint if needed
                    sh "sleep 10" // Wait for the container to start
                    sh "curl -f http://0.0.0.0:8000 || exit 1"

                    // Clean up
                    sh "docker stop prod_container && docker rm prod_container"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            cleanWs()
        }
    }
}