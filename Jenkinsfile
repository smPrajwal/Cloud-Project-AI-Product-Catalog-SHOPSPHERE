def APP_URL = ''
pipeline {
    agent any
    environment {
        TF_TOKEN_app_terraform_io = credentials('tfc-token')
        SHOPSPHERE_APP_ADMIN_PWD = credentials('ShopSphere_App_Admin_Password')
        AZURE_CLIENT_ID       = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET   = credentials('AZURE_CLIENT_SECRET')
        AZURE_TENANT_ID       = credentials('AZURE_TENANT_ID')
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_VM_PASSWORD = credentials('vm_password')
        AZURE_SQL_PASSWORD = credentials('db_password')
        STORAGE_ACCOUNT_NAME = 'shopsphereappsa'
        CODE_CONTAINER_NAME = 'application-code'
        AZURE_FUNCTIONAPP_NAME = 'azure-ai-function-app'
        FRONTEND_APP_CODE = 'project1_shopsphere_frontend.zip'
        BACKEND_APP_CODE = 'project1_shopsphere_backend.zip'
    }
    parameters {
        choice(name: 'Run_type',
        choices: ['Clone and Package (CI)', 'Deploy Infrastructure and Application (CD)', 'Full Pipeline (CICD)', 'De-provision Infrastructure and Application'],
        description: 'This is used to select the part of pipeline to run')
    }
    stages {
        stage('Pre-build Validation') {
            when {
                expression {params.Run_type == 'Clone and Package (CI)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "-------------------------------------- Started Testing!... -------------------------------"
                sh """
                    set -e

                    test -d Azure_Function
                    test -d Azure_Terraform
                    test -d static
                    test -d templates
                    test -d backend_pkg
                    test -d frontend_pkg
                    test -d shared_pkg
                    test -d database
                    test -f app.py
                    test -f startup.sh
                    test -f requirements_backend.txt
                    test -f requirements_frontend.txt
                """
                echo "----------------------- Testing Completed: All Checks passed in Testing! -----------------"
            }
        }

        stage('Packaging') {
            when {
                expression {params.Run_type == 'Clone and Package (CI)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "------------------------------------ Started Packaging!... -------------------------------"
                sh """
                    zip -r ${FRONTEND_APP_CODE} app.py startup.sh requirements_frontend.txt frontend_pkg shared_pkg templates static -x "static/product_images*"
                    zip -r ${BACKEND_APP_CODE} app.py startup.sh requirements_backend.txt backend_pkg shared_pkg database
                    test -f ${FRONTEND_APP_CODE}
                    test -f ${BACKEND_APP_CODE}
                """
                echo "-------------------- Packaging Completed: files have been Packaged! -----------------"
            }
        }

        stage('Push to Artifacts') {
            when {
                expression {params.Run_type == 'Clone and Package (CI)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "----------------------- Started Archiving to Jenkins Artifact!... ------------------------"
                archiveArtifacts artifacts: "${FRONTEND_APP_CODE}, ${BACKEND_APP_CODE}"
                echo "-------------------- Archiving Completed: Artifact has been pushed! ----------------------"
            }
        }

        stage('Manual Approval') {
            when {
                expression {params.Run_type != 'Clone and Package (CI)'}
            }
            steps {
                echo "-------------------------- Waiting for manual approval!... -------------------------------"
                input message: 'Approve to add/modify the Infrastructure and Application'
                echo "--------------------- Approval Completed: Successfully Approved! -------------------------"
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
                filter: "${FRONTEND_APP_CODE}, ${BACKEND_APP_CODE}"
                )
                sh """
                    test -f ${FRONTEND_APP_CODE}
                    test -f ${BACKEND_APP_CODE}
                """
                echo "----------- Pulled the Artifact: The Artifact is ready in the workspace! -----------------"
            }
        }

        stage('Creating Resources using Terraform') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "--------------- Started Building the Infrastructure using Terraform!... ------------------"
                withEnv([
                    "TF_VAR_app_admin_pwd=${SHOPSPHERE_APP_ADMIN_PWD}",
                    "TF_VAR_vm_pwd=${AZURE_VM_PASSWORD}",
                    "TF_VAR_db_pwd=${AZURE_SQL_PASSWORD}",
                    "TF_VAR_sa_name=${STORAGE_ACCOUNT_NAME}",
                    "TF_VAR_code_blob_container_name=${CODE_CONTAINER_NAME}",
                    "TF_VAR_function_app_name=${AZURE_FUNCTIONAPP_NAME}",
                    "TF_VAR_frontend_code_blob_url=https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net/${CODE_CONTAINER_NAME}/frontend/${FRONTEND_APP_CODE}",
                    "TF_VAR_backend_code_blob_url=https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net/${CODE_CONTAINER_NAME}/backend/${BACKEND_APP_CODE}"
                ]) {
                    sh """
                        cd Azure_Terraform
                        terraform init -input=false
                        terraform fmt -check -recursive
                        terraform validate
                        terraform plan
                        terraform apply -auto-approve
                    """
                }
                script {
                    def ip = sh(
                        script: 'cd Azure_Terraform && terraform output -raw application_public_ip',
                        returnStdout: true
                    ).trim()
                    APP_URL = "http://${ip}:80"
                }
                echo "--------- Infrastructure Building Completed: Infrastructure is built and ready! ----------"
            }
        }

        stage('Azure Authentication using Service Principal') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "------------ Authenticating with Azure using Azure Service Principal! --------------------"
                sh """
                    az login --service-principal \
                    --username "$AZURE_CLIENT_ID" \
                    --password "$AZURE_CLIENT_SECRET" \
                    --tenant "$AZURE_TENANT_ID"

                    az account set --subscription "$AZURE_SUBSCRIPTION_ID"
                """
                echo "------- Authenticating completed: Successfully Authenticated with Azure! -----------------"
            }
        }

        stage('Uploading files to Azure Blob Container') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo " ---------------- Started uploading files to Azure Blob Container ---------------------"
                sh """
                    az storage blob upload \
                    --account-name "$STORAGE_ACCOUNT_NAME" \
                    --container-name "$CODE_CONTAINER_NAME" \
                    --name frontend/${FRONTEND_APP_CODE} \
                    --file ${FRONTEND_APP_CODE} \
                    --overwrite

                    az storage blob upload \
                    --account-name "$STORAGE_ACCOUNT_NAME" \
                    --container-name "$CODE_CONTAINER_NAME" \
                    --name backend/${BACKEND_APP_CODE} \
                    --file ${BACKEND_APP_CODE} \
                    --overwrite

                    echo "Uploading Product Images..."
                    az storage blob upload-batch \
                    --account-name "$STORAGE_ACCOUNT_NAME" \
                    --destination "product-images" \
                    --source static/product_images \
                    --overwrite       
                """
                echo "-------- Upload Completed: Files have been uploaded to the Azure Blob Container --------------"
            }
        }

        stage('Configuration and Deployment to Azure Function') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "------------------- Started to Configure and deploy the code to Azure Function!... ---------------------------------"
                sh """
                    cd Azure_Function
                    func azure functionapp publish ${AZURE_FUNCTIONAPP_NAME} --python
                    echo "------ Testing Azure Function code Deployment ------"
                    func azure functionapp list-functions ${AZURE_FUNCTIONAPP_NAME}
                """
                echo "---------- Azure Function Configuration Completed: The Azure function is ready to be triggered through Blob upload! ----------------"
            }
        }

        stage('Logout from Service Principal') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "Logging out from the Service Principal"
                sh """
                    az logout || true
                """
                echo "Logout Successful: Logged out from the Service Principal"
            }
        }

        stage('Smoke Testing') {
            when {
                expression {params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "------------------------- Started Smoke Testing!... --------------------------------------"
                sh """
                    set -e
                    URL="${APP_URL}"

                    curl --fail --max-time 10 "\$URL/health"

                    curl -s --max-time 10 "\$URL" | grep -q "ShopSphere"
                """
                echo "--------- Smoke Testing Completed: The application is LIVE and working! ------------------"
            }
        }

        stage('Removing the complete Infrastructure, Resources and Application') {
            when {
                expression {params.Run_type == 'De-provision Infrastructure and Application'}
            }
            steps {
                echo "------- Started Tear down of the complete Infrastructure and Application -----------------"
                withEnv([
                    "TF_VAR_app_admin_pwd=${SHOPSPHERE_APP_ADMIN_PWD}",
                    "TF_VAR_vm_pwd=${AZURE_VM_PASSWORD}",
                    "TF_VAR_db_pwd=${AZURE_SQL_PASSWORD}",
                    "TF_VAR_sa_name=${STORAGE_ACCOUNT_NAME}",
                    "TF_VAR_code_blob_container_name=${CODE_CONTAINER_NAME}",
                    "TF_VAR_function_app_name=${AZURE_FUNCTIONAPP_NAME}",
                    "TF_VAR_frontend_code_blob_url=https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net/${CODE_CONTAINER_NAME}/frontend/${FRONTEND_APP_CODE}",
                    "TF_VAR_backend_code_blob_url=https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net/${CODE_CONTAINER_NAME}/backend/${BACKEND_APP_CODE}"
                ]) {
                    sh """
                        cd Azure_Terraform
                        terraform init -input=false
                        terraform destroy -auto-approve
                    """
                }
                echo "------- Infrastructure Tear down Completed: The Complete Infrastructure (with all the Resources) have been Cleaned-up -------"
            }
        }
    }
    post {
        always {
            script {
                def extraContent  = ""
                if ((params.Run_type == 'Deploy Infrastructure and Application (CD)' || params.Run_type == 'Full Pipeline (CICD)') && currentBuild.currentResult == 'SUCCESS') {
                    extraContent += """
                        <br/>
                        Click here to access the application: 
                        <a href="${APP_URL}">Open application</a>
                    """
                }
                emailext (
                    to: '$DEFAULT_RECIPIENTS',
                    subject: '$DEFAULT_SUBJECT',
                    attachLog: true, 
                    compressLog: true,
                    mimeType: 'text/html',
                    body: """
                        <b>The Pipeline was executed using the below Parameter:</b><br/>
                        Run_type: ${params.Run_type}
                        <br/><br/>
                        \$DEFAULT_CONTENT
                        ${extraContent}
                    """
                )
            }
            cleanWs()
            echo "--------- Workspace cleaned!!! ---------"
        }
    }
}