// Jenkinsfile - the automation recipe for AutoCart
//
// What this does, in plain words:
// 1. Pull the latest code from GitHub
// 2. Build fresh Docker images for catalog, order, and frontend services
// 3. Push those images to Docker Hub
// 4. Tell Kubernetes to apply the latest manifests (including the
//    products-config ConfigMap, if it changed)
// 5. Restart the deployments so they pick up new images/config
//
// Trigger: manually for now (click "Build Now"), webhook automation comes later.

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
                // Pulls the latest code from your GitHub repo.
                // Since it's public, no credentials needed here.
                git branch: 'master',
                    url: 'https://github.com/kummethavanitha/shopping_cart.git'
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    docker build -t $DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG ./catalog-service
                    docker build -t $DOCKERHUB_USERNAME/order-service:$IMAGE_TAG ./order-service
                    docker build -t $DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG ./frontend-service
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push $DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG
                    docker push $DOCKERHUB_USERNAME/order-service:$IMAGE_TAG
                    docker push $DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/00-namespaces.yaml
                    kubectl apply -f k8s/04-configmap.yaml
                    kubectl apply -f k8s/01-catalog-service.yaml
                    kubectl apply -f k8s/02-order-service.yaml
                    kubectl apply -f k8s/03-frontend-service.yaml

                    kubectl set image deployment/catalog-service catalog-service=$DOCKERHUB_USERNAME/catalog-service1:$IMAGE_TAG -n catalog
                    kubectl set image deployment/order-service order-service=$DOCKERHUB_USERNAME/order-service:$IMAGE_TAG -n order
                    kubectl set image deployment/frontend frontend=$DOCKERHUB_USERNAME/frontend-service:$IMAGE_TAG -n frontend
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

    post {
        success {
            echo "✅ AutoCart deployed successfully with image tag: ${IMAGE_TAG}"
        }
        failure {
            echo "❌ Pipeline failed - check the stage logs above."
        }
    }
}

