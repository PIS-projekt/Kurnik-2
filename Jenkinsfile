pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = "docker-compose.yaml"
        DOCKER_BACKEND_TESTS = "backend-tests"
        DOCKER_BACKEND_PROD = "backend"
    }


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
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE run --rm $DOCKER_BACKEND_TESTS"
                }
            }
        }

        stage('Linting and Formatting') {
            steps {
                script {
                    // Adjust the linting/formatting tools as per your setup
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE run --rm $DOCKER_BACKEND_TESTS pdm run lint"
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE run --rm $DOCKER_BACKEND_TESTS pdm run format"
                }
            }
        }

        stage('Build for Production') {
            steps {
                script {
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE build $DOCKER_BACKEND_PROD"
                }
            }
        }

        stage('Verify Production Build') {
            steps {
                script {
                    // Verify the production build by running it temporarily
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE up -d $DOCKER_BACKEND_PROD"

                    // Run a health check or test endpoint if needed
                    sh "sleep 10" // Wait for the container to start
                    sh "curl -f http://localhost:8000 || exit 1"

                    // Clean up
                    sh "docker-compose -f $DOCKER_COMPOSE_FILE down"
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
