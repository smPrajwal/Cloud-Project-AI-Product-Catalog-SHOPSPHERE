pipeline {
    agent any
    stages {
        stage('Testing') {
            steps {
                sh '''
                    set -e

                    echo "Testing Started"

                    python3 -m compileall .

                    test -d static
                    test -d templates
                    test -d backend
                    test -f app.py
                    test -f startup.sh
                    test -f requirements.txt

                    echo "All Checks passed in Testing!"
                '''
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
        stage('Testing') {
            steps {
                
            }
        }
    }
}