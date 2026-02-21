def APP_URL = ''
pipeline {
    agent any
    environment {
        TF_TOKEN_app_terraform_io = credentials('tfc-token')
        TF_VAR_app_admin_pwd = credentials('ShopSphere_App_Admin_Password')
        AZURE_CLIENT_ID       = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET   = credentials('AZURE_CLIENT_SECRET')
        AZURE_TENANT_ID       = credentials('AZURE_TENANT_ID')
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        TF_VAR_vm_pwd = credentials('vm_password')
        TF_VAR_db_pwd = credentials('db_password')
        TF_VAR_sa_name = 'ssapplicationstorageacc'
        TF_VAR_code_container = 'application-code'
        TF_VAR_function_app_name = 'azure-vision-ai-function-app-ss'
        TF_VAR_frontend_code = 'project1_shopsphere_frontend.zip'
        TF_VAR_backend_code = 'project1_shopsphere_backend.zip'
        TF_VAR_default_loc = 'centralindia'
        TF_VAR_vm_sku = 'Standard_B2pls_v2'
    }
    parameters {
        choice(name: 'RUN_TYPE',
        choices: ['Clone and Package (CI)', 'Deploy Infrastructure and Application (CD)', 'Full Pipeline (CICD)', 'De-provision Infrastructure and Application'],
        description: 'This is used to select the part of pipeline to run')
    }
    stages {
        stage('Pre-build Validation') {
            when {
                expression {params.RUN_TYPE == 'Clone and Package (CI)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "-------------------------------------- Started Testing!... -------------------------------"
                sh """
                    set -e

                    test -d Azure_Function
                    test -d Azure_Terraform
                    test -d backend
                    test -d common
                    test -d database
                    test -d frontend
                    test -f app.py
                    test -f requirements_backend.txt
                    test -f requirements_frontend.txt
                """
                echo "----------------------- Testing Completed: All Checks passed in Testing! -----------------"
            }
        }

        stage('Packaging') {
            when {
                expression {params.RUN_TYPE == 'Clone and Package (CI)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "------------------------------------ Started Packaging!... -------------------------------"
                sh """
                    zip -r ${TF_VAR_frontend_code} app.py requirements_frontend.txt frontend common -x "frontend/static/product_images*"
                    zip -r ${TF_VAR_backend_code} app.py requirements_backend.txt backend common database
                    test -f ${TF_VAR_frontend_code}
                    test -f ${TF_VAR_backend_code}
                """
                echo "-------------------- Packaging Completed: files have been Packaged! -----------------"
            }
        }

        stage('Push to Artifacts') {
            when {
                expression {params.RUN_TYPE == 'Clone and Package (CI)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "----------------------- Started Archiving to Jenkins Artifact!... ------------------------"
                archiveArtifacts artifacts: "${TF_VAR_frontend_code}, ${TF_VAR_backend_code}"
                echo "-------------------- Archiving Completed: Artifact has been pushed! ----------------------"
            }
        }

        stage('Manual Approval') {
            when {
                expression {params.RUN_TYPE != 'Clone and Package (CI)'}
            }
            steps {
                echo "-------------------------- Waiting for manual approval!... -------------------------------"
                input message: 'Approve to add/modify the Infrastructure and Application'
                echo "--------------------- Approval Completed: Successfully Approved! -------------------------"
            }
        }

        stage('Pull from Artifacts') {
            when {
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)'}
            }
            steps {
                echo "------------------------ Started pulling the Artifact!... --------------------------------"
                copyArtifacts(
                projectName: env.JOB_NAME,
                selector: lastWithArtifacts(),
                filter: "${TF_VAR_frontend_code}, ${TF_VAR_backend_code}"
                )
                sh """
                    test -f ${TF_VAR_frontend_code}
                    test -f ${TF_VAR_backend_code}
                """
                echo "----------- Pulled the Artifact: The Artifact is ready in the workspace! -----------------"
            }
        }

        stage('Creating Resources using Terraform') {
            when {
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "--------------- Started Building the Infrastructure using Terraform!... ------------------"
                sh """
                    cd Azure_Terraform
                    terraform init -input=false
                    terraform fmt -check -recursive
                    terraform validate
                    terraform plan
                    terraform apply -auto-approve
                """
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
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
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
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo " ---------------- Started uploading files to Azure Blob Container ---------------------"
                sh """
                    az storage blob upload \
                    --account-name "$TF_VAR_sa_name" \
                    --container-name "$TF_VAR_code_container" \
                    --name frontend/${TF_VAR_frontend_code} \
                    --file ${TF_VAR_frontend_code} \
                    --overwrite

                    az storage blob upload \
                    --account-name "$TF_VAR_sa_name" \
                    --container-name "$TF_VAR_code_container" \
                    --name backend/${TF_VAR_backend_code} \
                    --file ${TF_VAR_backend_code} \
                    --overwrite

                    echo "Uploading Product Images..."
                    az storage blob upload-batch \
                    --account-name "$TF_VAR_sa_name" \
                    --destination "product-images" \
                    --source frontend/static/product_images \
                    --overwrite
                """
                echo "-------- Upload Completed: Files have been uploaded to the Azure Blob Container --------------"
            }
        }

        stage('Configuration and Deployment to Azure Function') {
            when {
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
            }
            steps {
                echo "Waiting for Function App SCM Warm-up..."
                sleep 90
                echo "------------------- Started to Configure and deploy the code to Azure Function!... ---------------------------------"
                retry(3) {
                    sh """
                        cd Azure_Function
                        func azure functionapp publish ${TF_VAR_function_app_name} --python
                        echo "------ Testing Azure Function code Deployment ------"
                        func azure functionapp list-functions ${TF_VAR_function_app_name}
                    """
                }
                echo "---------- Azure Function Configuration Completed: The Azure function is ready to be triggered through Blob upload! ----------------"
            }
        }

        stage('Logout from Service Principal') {
            when {
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
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
                expression {params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)'}
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
                expression {params.RUN_TYPE == 'De-provision Infrastructure and Application'}
            }
            steps {
                echo "------- Started Tear down of the complete Infrastructure and Application -----------------"
                sh """
                    cd Azure_Terraform
                    terraform init -input=false
                    terraform destroy -auto-approve
                """
                echo "------- Infrastructure Tear down Completed: The Complete Infrastructure (with all the Resources) have been Cleaned-up -------"
            }
        }
    }
    post {
        always {
            script {
                def extraContent  = ""
                if ((params.RUN_TYPE == 'Deploy Infrastructure and Application (CD)' || params.RUN_TYPE == 'Full Pipeline (CICD)') && currentBuild.currentResult == 'SUCCESS') {
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
                    body: """
                        <b>The Pipeline was executed using the below Parameter:</b><br/>
                        RUN_TYPE: ${params.RUN_TYPE}
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