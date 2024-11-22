pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'cd frontend'
            }
        }

        stage('Setup node and install frontend dependencies') {
            steps {
                nodejs(nodeJSInstallationName: 'node-23') {
                    sh 'npm install'
                }

                script {
                    echo 'Workspace Contents:'
                    sh 'ls -la'
                }
            }
        }

        stage('Lint frontend') {
            steps {
                script {
                    echo 'Running ESLint...'
                    sh 'npm run lint'
                }
            }
        }

        stage('Run frontend tests') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'npm run test'
                }
            }
        }

        stage('Build frontend') {
            steps {
                script {
                    echo 'Building the project...'
                    sh 'npm run build'
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
