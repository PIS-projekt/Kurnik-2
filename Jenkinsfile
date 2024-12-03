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
                frontend-build = docker.build("frontend-image:${env.BUILD_ID}", '-f Dockerfile')
            }
        }

        stage('Upload frontend image to Nexus') {
            steps {
                docker.withRegistry('nexus.mgarbowski.pl', 'nexus-registry-credentials') {
                    frontend-build.push("${env.BUILD_NUMBER}")
                    frontend-build.push("latest")
                }

            }
        }

        stage('Build Backend Image') {
            steps {
                script {
                    customImage = docker.build("backend-image:${env.BUILD_ID}", '-f backend/Dockerfile backend/')
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                script {
                    customImage.inside {
                        sh 'pdm run test'
                    }
                }
            }
        }

        stage('Lint Backend') {
            steps {
                script {
                    customImage.inside {
                        sh 'pdm run lint'
                    }
                }
            }
        }

        stage('Generate Test Coverage Report') {
            steps {
                script {
                    customImage.inside {
                        sh 'pdm run coverage'
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
