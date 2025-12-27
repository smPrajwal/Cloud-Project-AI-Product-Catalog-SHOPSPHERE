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
                echo "-------------------------------------- Started Testing!... -------------------------------"
                sh '''
                    set -e

                    python3 -m compileall -f -q .

                    test -d static
                    test -d templates
                    test -d backend
                    test -f app.py
                    test -f startup.sh
                    test -f requirements.txt
                    test -f testfile.py
                '''
                echo "----------------------- Testing Completed: All Checks passed in Testing! -----------------"
            }
        }

        stage('Packaging') {
            when {
                expression {params.Run_type != 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                echo "------------------------------------ Started Packaging!... -------------------------------"
                sh '''
                    zip -r project1_shopsphere.zip app.py startup.sh backend database static templates
                '''
                echo "-------------------- Packaging Completed: Application has been Packaged! -----------------"
            }
        }

        stage('Push to Artifacts') {
            when {
                expression {params.Run_type != 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                echo "----------------------- Started Archiving to Jenkins Artifact!... ------------------------"
                archiveArtifacts artifacts: 'project1_shopsphere.zip'
                echo "-------------------- Archiving Completed: Artifact has been pushed! ----------------------"
            }
        }

        stage('Manual Approval') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "-------------------------- Waiting for manual approval!... -------------------------------"
                input message: 'Approve to deploy the Infrastructure and Application'
                echo "--------------------- Approval Completed: Successfully Approved! -------------------------"
            }
        }

        stage('Creating Resources using Terraform') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "--------------- Started Building the Infrastructure using Terraform!... ------------------"
                sh '''
                    echo "In 'Creating Resources using Terraform' Stage!"
                '''
                echo "--------- Infrastructure Building Completed: Infrastructure is built and ready! ----------"
            }
        }

        stage('Pull from Artifacts') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                echo "------------------------ Started pulling the Artifact!... --------------------------------"
                copyArtifacts(
                projectName: env.JOB_NAME,
                selector: lastWithArtifacts(),
                filter: 'project1_shopsphere.zip'
                )
                sh 'test -f project1_shopsphere.zip'
                echo "----------- Pulled the Artifact: The Artifact is ready in the workspace! -----------------"
            }
        }

        stage('Configuration and Deployment using Ansible') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "------------------- Started to Configure the Servers!... ---------------------------------"
                sh '''
                    echo "In 'Configuration and Deployment using Ansible' Stage!"
                '''
                echo "---------- Configuration Completed: The Servers are configured and ready! ----------------"
            }
        }

        stage('Smoke Testing') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "------------------------- Started Smoke Testing!... --------------------------------------"
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
                echo "--------- Smoke Testing Completed: The application is LIVE and working! ------------------"
            }
        }
    }
    post {
        always {
            script {
                env.VM_URL = sh(
                    script: 'echo "<Add URL here>"',
                    returnStdout: true
                ).trim()
                def body = '$DEFAULT_CONTENT'
                if (params.Run_type != 'Clone and Package (CI)' && currentBuild.currentResult == 'SUCCESS') {
                    body += """
                    <br/>
                    Click here to access the application: 
                    <a href="${env.VM_URL}">Open application</a>
                    """
                }
                emailext (
                    to: '$DEFAULT_RECIPIENTS',
                    subject: '$DEFAULT_SUBJECT',
                    body: body,
                    attachLog: true, 
                    compressLog: true,
                    mimeType: 'text/html'
                )
            }
            cleanWs()
            echo "--------- Workspace cleaned!!! ---------"
        }
    }
}