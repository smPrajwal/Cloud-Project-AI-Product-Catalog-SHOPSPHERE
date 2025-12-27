pipeline {
    agent any
    environment {
        VM_URL = ''
    }
    parameters {
        choice(name: 'Run_type',
        choices: ['Clone and Package (CI)', 'Deploy Infrastructure and Application (CD)', 'Full Pipeline (CICD)'],
        description: 'This is used to select the part of pipeline to run')
    }
    stages {
        stage('Testing') {
            when {
                expression {params.Run_type != 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                echo "Testing Started..."
                sh '''
                    set -e

                    python3 -m compileall .

                    test -d static
                    test -d templates
                    test -d backend
                    test -f app.py
                    test -f startup.sh
                    test -f requirements.txt
                '''
                echo "All Checks passed in Testing!"
            }
        }

        stage('Packaging') {
            when {
                expression {params.Run_type != 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                sh '''
                    zip -r project1_shopsphere.zip app.py startup.sh backend database static templates
                '''
                echo "Application has been Packaged"
            }
        }

        stage('Push to Artifacts') {
            when {
                expression {params.Run_type != 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                archiveArtifacts artifacts: 'project1_shopsphere.zip'
                echo "Artifact has been pushed"
            }
        }

        stage('Manual Approval') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                input message: 'Approve to deploy the Infrastructure and Application'
            }
        }

        stage('Creating Resources using Terraform') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                sh '''
                    echo "In 'Creating Resources using Terraform' Stage"
                '''
            }
        }

        stage('Pull from Artifacts') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                copyArtifacts(
                projectName: env.JOB_NAME,
                selector: lastSuccessful(),
                filter: 'project1_shopsphere.zip'
                )
                sh 'test -f project1_shopsphere.zip'
                echo "Pulled the Artifact"
            }
        }

        stage('Configuration and Deployment using Ansible') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                sh '''
                    echo "In 'Configuration and Deployment using Ansible' Stage"
                '''
            }
        }

        stage('Smoke Testing') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "Smoke Test Started..."
                // sh '''
                //     set -e
                //     URL="${env.VM_URL}"

                //     curl --fail --max-time 10 "$URL/health"

                //     curl -s --max-time 10 "$URL" | grep -q "ShopSphere"
                // '''
                // echo "SMOKE TEST PASSED: Website is LIVE and working!"

                // //Sleeping for the mentioned amount of time
                // echo "Sleeping for amount of time, before destroying all the Terraform resources"
                // sleep time: 10, unit: 'MINUTES'
            }
        }
    }
    post {
        always {
            def body = ""
            script {
                env.VM_URL = sh(
                    script: 'echo "<Add URL here>"',
                    returnStdout: true
                ).trim()
                body = '$DEFAULT_CONTENT'
                if (params.Run_type != 'Clone and Package (CI)' && currentBuild.currentResult == 'SUCCESS') {
                    body += """
                    <br/>
                    Click here to access the application: 
                    <a href="${env.VM_URL}">Open application</a>
                    """
                }
            }
            emailext (
                subject: '$DEFAULT_SUBJECT',
                body: body,
                mimeType: 'text/html'
            )
            cleanWs()
            echo "Workspace cleaned."
        }
    }
}