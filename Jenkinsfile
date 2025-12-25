pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Unit Test') {
            steps {
                // Trivial placeholder for interview demo
                echo 'Running unit tests...'
                // sh 'python3 -m pytest' // if tests existed
                echo 'No tests found (Skipped)'
            }
        }
        
        stage('Package') {
            steps {
                echo 'Packaging application...'
                // Simple zip of the required artifacts
                sh 'zip -r artifact.zip app.py templates/ static/ requirements.txt'
            }
        }
    }
}
