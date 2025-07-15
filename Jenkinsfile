pipeline {
    agent any

    stages {
        stage('Git Pull') {
            steps {
                    git branch: 'main', url: 'https://github.com/PavanAmbuskar/flask.git'            }
        }

        stage('Test PowerShell') {
            steps {
                powershell 'Write-Output "PowerShell is working!"'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t pavanambuskar/flask-k8s .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                    bat 'docker push pavanambuskar/flask-k8s'
                }
            }
        }

        stage('Deploy Flask via SSM') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-cred-id']
                ]) {
                    powershell '''
                        # Step 1: Define commands array as a string for inline JSON
                        $cmds = '["docker pull pavanambuskar/flask-k8s","docker rm -f flask || true","docker run -d --name flask -p 80:5000 
                                    pavanambuskar/flask-k8s"]'
        
                        # Step 2: Use AWS CLI with correct --parameters key=value format
                        aws ssm send-command `
                            --document-name "AWS-RunShellScript" `
                            --comment "DeployFlask" `
                            --instance-ids "i-0c0db149ec396d4c4" `
                            --parameters "commands=$cmds" `
                            --region "us-east-1"
                    '''
                }
            }
        }


    }
}