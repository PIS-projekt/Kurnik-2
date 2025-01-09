pipeline {
    agent any

    stages {


        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        // stage('Setup node and install frontend dependencies') {
        //     steps {
        //         dir('frontend') {
        //             nodejs(nodeJSInstallationName: 'node-23') {
        //                 sh 'npm install'
        //             }
        //         }
        //     }
        // }

        // stage('Lint frontend') {
        //     steps {
        //         dir('frontend') {
        //             nodejs(nodeJSInstallationName: 'node-23') {
        //                 script {
        //                     echo 'Running ESLint...'
        //                     sh 'npm run lint'
        //                 }
        //             }
        //         }
        //     }
        // }

        // stage('Run frontend tests') {
        //     steps {
        //         dir('frontend') {
        //             nodejs(nodeJSInstallationName: 'node-23') {
        //                 script {
        //                     echo 'Running tests...'
        //                     sh 'npm run test'
        //                 }
        //             }
        //         }
        //     }
        // }

        // stage('Build frontend') {
        //     steps {
        //         // dir('frontend') {
        //         //     nodejs(nodeJSInstallationName: 'node-23') {
        //         //         script {
        //         //             echo 'Building the project...'
        //         //             sh 'npm run build'
        //         //         }
        //         //     }
        //         // }
        //         script {
        //             frontend_build = docker.build("docker-images/pis-frontend", '-f frontend/Dockerfile frontend/')
        //         }
        //     }
        // }

        // stage('Upload frontend image to Nexus') {
        //     steps {
        //         script {
        //             docker.withRegistry('https://nexus.mgarbowski.pl', 'nexus-registry-credentials') {
        //                 frontend_build.push("latest")
        //             }
        //         }

        //     }
        // }


        // stage('Build for Testing') {
        //     steps {
        //         script {
        //             sh "docker build --target test -t backend-tests -f backend/Dockerfile backend/"
        //         }
        //     }
        // }

        // stage('Run Tests') {
        //     steps {
        //         script {
        //             sh "docker run --rm backend-tests"
        //         }
        //     }
        // }

        // stage('Test Coverage') {
        //     steps {
        //         script {
        //             sh "docker run --rm backend-tests pdm run coverage"
        //         }
        //     }
        // }

        // stage('Linting and Formatting') {
        //     steps {
        //         script {
        //             // Adjust the linting/formatting tools as per your setup
        //             sh "docker run --rm backend-tests pdm run lint"
        //             sh "docker run --rm backend-tests pdm run format"
        //         }
        //     }
        // }

        // stage('Build for Production') {
        //     steps {
        //         script {
        //             backend_build = docker.build("docker-images/pis-backend", "--target prod -f backend/Dockerfile backend")
        //             echo "Done building"
        //         }
        //     }
        // }

        // stage('Verify Production Build') {
        //     steps {
        //         script {
        //             echo "Starting the production container from the built image..."

        //             // Start the container
        //             def prodContainer = backend_build.run("-p 8000:8000")
        //             def containerId = prodContainer.id

        //             try {
        //                 // Run a health check or test endpoint
        //                 echo "Waiting for the container to initialize..."
        //                 sleep(10) // Adjust sleep time as needed
        //                 sh "curl -f http://0.0.0.0:8000 || exit 1"
        //             } finally {
        //                 // Clean up the container using shell commands
        //                 echo "Stopping and removing the container..."
        //                 sh "docker stop ${containerId}"
        //                 sh "docker rm -f ${containerId}"
        //             }
        //         }
        //     }
        // }

        // stage('Upload backend image to Nexus') {
        //     steps {
        //         script {
        //             docker.withRegistry('https://nexus.mgarbowski.pl', 'nexus-registry-credentials') {
        //                 backend_build.push("latest")
        //             }
        //         }

        //     }
        // }

        stage('deploy to production') {
            // when {
            //     branch 'SCRUM-37-Deployment-on-remote-server-script'
            // }
            stages {
                stage('Get user confirmation') {
                    steps {
                        script {
                            def userInput = input(
                                id: 'userInput',
                                message: 'Do you want to deploy to production?',
                                parameters: [
                                    booleanParam(defaultValue: false, description: 'Deploy to production?', name: 'deployToProduction')
                                ]
                            )
                            if (!userInput.deployToProduction) {
                                error('Production deployment cancelled by the user')
                            }
                        }
                    }
                }
                stage('Deploy to production') {
                    steps {
                        script {
                            echo 'Deploying to production...'
                            // Add deployment steps here
                        }
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
