pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-northeast-1'

        // ECR 정보
        ECR_REGISTRY = '050314037804.dkr.ecr.ap-northeast-1.amazonaws.com'
        ECR_REPO = "${ECR_REGISTRY}/be-django"
        IMAGE_NAME = 'be-django'

        // ECS 정보
        ECS_CLUSTER = 'Ix4-be-cluster'
        ECS_SERVICE = 'be-django-service'
        TASK_DEFINITION_NAME = 'task-definition-BE-django'
        CONTAINER_NAME = 'be-django-container'
        EXECUTION_ROLE_ARN = 'arn:aws:iam::050314037804:role/ecsTaskExecutionRole' 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/lgcns-2nd-project-Ix4/cryptory-django.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t $IMAGE_NAME .
                    docker tag $IMAGE_NAME:latest $ECR_REPO:latest
                """
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'AWS-CREDENTIALS'
                ]]) {
                    sh """
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $ECR_REGISTRY
                    """
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh "docker push $ECR_REPO:latest"
            }
        }

        stage('Register ECS Task Definition') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'AWS-CREDENTIALS'
                ]]) {
                    script {
                        def registerOutput = sh(
                            script: """
                                aws ecs register-task-definition \
                                    --family $TASK_DEFINITION_NAME \
                                    --requires-compatibilities FARGATE \
                                    --network-mode awsvpc \
                                    --execution-role-arn $EXECUTION_ROLE_ARN \\
                                    --cpu "256" \
                                    --memory "512" \
                                    --container-definitions '[
                                        {
                                            "name": "$CONTAINER_NAME",
                                            "image": "$ECR_REPO:latest",
                                            "essential": true,
                                            "portMappings": [
                                                {
                                                    "containerPort": 8000,
                                                    "protocol": "tcp"
                                                }
                                            ]
                                        }
                                    ]' \
                                    --region $AWS_REGION \
                                    --output json
                            """,
                            returnStdout: true
                        ).trim()

                        def taskDefArn = new groovy.json.JsonSlurperClassic()
                            .parseText(registerOutput)
                            .taskDefinition
                            .taskDefinitionArn

                        env.TASK_DEF_ARN = taskDefArn
                    }
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'AWS-CREDENTIALS'
                ]]) {
                    sh """
                        aws ecs update-service \
                            --cluster $ECS_CLUSTER \
                            --service $ECS_SERVICE \
                            --task-definition $TASK_DEF_ARN \
                            --force-new-deployment \
                            --region $AWS_REGION
                    """
                }
            }
        }
    }
}