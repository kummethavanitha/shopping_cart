pipeline {

    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        DOCKERHUB_USERNAME    = 'vanitha2612'
        IMAGE_TAG             = "build-${BUILD_NUMBER}"
    }


    stages {


        stage('Checkout') {
            steps {

                git branch: 'master',
                    url: 'https://github.com/kummethavanitha/shopping_cart.git'

            }
        }



        stage('Detect Changes') {

            steps {

                script {

                    def changes = sh(
                        script: "git diff --name-only HEAD~1 HEAD",
                        returnStdout: true
                    ).trim()


                    echo "Changed files:"
                    echo changes


                    if(changes.contains("k8s/04-configmap.yaml")
                       && !changes.contains("catalog-service")
                       && !changes.contains("order-service")
                       && !changes.contains("frontend-service")){


                        env.CONFIG_ONLY = "true"

                    }

                    else {

                        env.CONFIG_ONLY = "false"

                    }

                }

            }

        }



        stage('Build Images') {

            when {

                expression {

                    env.CONFIG_ONLY == "false"

                }

            }


            steps {

                sh '''

                docker build -t $DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG ./catalog-service

                docker build -t $DOCKERHUB_USERNAME/order-service:$IMAGE_TAG ./order-service

                docker build -t $DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG ./frontend-service


                '''

            }

        }




        stage('Push Images') {


            when {

                expression {

                    env.CONFIG_ONLY == "false"

                }

            }


            steps {


                sh '''

                echo $DOCKERHUB_CREDENTIALS_PSW | docker login \
                -u $DOCKERHUB_CREDENTIALS_USR --password-stdin


                docker push $DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG

                docker push $DOCKERHUB_USERNAME/order-service:$IMAGE_TAG

                docker push $DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG


                '''

            }

        }





        stage('Deploy ConfigMap') {


            when {

                expression {

                    env.CONFIG_ONLY == "true"

                }

            }


            steps {


                sh '''

                echo "Only ConfigMap changed"


                kubectl apply -f k8s/04-configmap.yaml


                kubectl rollout restart deployment/catalog-service -n catalog

                kubectl rollout restart deployment/order-service -n order

                kubectl rollout restart deployment/frontend -n frontend



                '''

            }

        }





        stage('Deploy Application') {


            when {

                expression {

                    env.CONFIG_ONLY == "false"

                }

            }


            steps {


                sh '''

                kubectl apply -f k8s/


                kubectl set image deployment/catalog-service \
                catalog-service=$DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG \
                -n catalog



                kubectl set image deployment/order-service \
                order-service=$DOCKERHUB_USERNAME/order-service:$IMAGE_TAG \
                -n order



                kubectl set image deployment/frontend \
                frontend=$DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG \
                -n frontend


                '''

            }

        }





        stage('Verify Rollout') {


            steps {


                sh '''

                kubectl rollout status deployment/catalog-service -n catalog --timeout=60s


                kubectl rollout status deployment/order-service -n order --timeout=60s


                kubectl rollout status deployment/frontend -n frontend --timeout=60s


                '''

            }

        }



    }


}
