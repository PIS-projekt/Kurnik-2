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
                script {
                    frontend_build = docker.build("docker-images/pis-frontend", '-f frontend/Dockerfile frontend/')
                }
            }
        }

        stage('Upload frontend image to Nexus') {
            steps {
                script {
                    docker.withRegistry('https://nexus.mgarbowski.pl', 'nexus-registry-credentials') {
                        frontend_build.push("latest")
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
                    backendBuild = docker.build("docker-images/pis-backend}", "--target prod -f backend/Dockerfile backend")
                }
            }
        }

        stage('Verify Production Build') {
            steps {
                script {
                    // Verify the production build using Docker plugin methods
                    echo "Starting the production container from the built image..."
                    
                    // Start the container
                    def prodContainer = backendBuild.run("-p 8000:8000")

                    try {
                        // Run a health check or test endpoint
                        echo "Waiting for the container to initialize..."
                        sleep(10) // Adjust sleep time as needed
                        prodContainer.exec(["curl", "-f", "http://0.0.0.0:8000"])
                    } finally {
                        // Clean up the container
                        echo "Stopping and removing the container..."
                        prodContainer.stop()
                        prodContainer.remove()
                    }
                }
            }
        }
        stage('Upload backend image to Nexus') {
            steps {
                script {
                    docker.withRegistry('https://nexus.mgarbowski.pl', 'nexus-registry-credentials') {
                        backendBuild.push("latest")
                    }
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