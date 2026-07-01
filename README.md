## 🏗️ Project Overview

AutoCart is a microservices-based e-commerce application built with three independent services:

- Catalog Service
- Order Service
- Frontend Service

Each service is containerized using Docker and deployed on Kubernetes.

The project implements a CI/CD pipeline using Jenkins, where changes pushed to GitHub automatically trigger image builds, Docker Hub updates, and Kubernetes deployments.

The application is developed and tested locally using VirtualBox and Minikube.

## 🏗️ Architecture

                         Developer
                             |
                             |
                      Push Code Changes
                             |
                             v
                    GitHub Repository
                             |
                             |
                    GitHub Webhook
                             |
                             v
                    Jenkins Pipeline
                             |
              --------------------------------
              |                              |
              |                              |
      Application Code Change          ConfigMap Change
              |                              |
              |                              |
              v                              v

      Build Docker Images            Apply ConfigMap Update
              |                       (Product prices)
              |
              v                              |
       Push Images to Docker Hub             |
              |                              |
              v                              v

      Update Kubernetes Image        Restart Deployment
              |                              |
              |                              |
              --------------------------------
                             |
                             v

                    Kubernetes Cluster
                             |
        ------------------------------------------------
        |                       |                      |
        v                       v                      v

  Catalog Service          Order Service          Frontend Service

  ## 🧩 The 3 Microservices


| Service | Namespace | Port | Responsibility |
|---|---|---|---|
| frontend-service | frontend | 5000 (NodePort 30080) | Web UI — displays products and accepts orders |
| catalog-service | catalog | 5001 | Serves product catalog and provides live prices from ConfigMap |
| order-service | order | 5002 | Accepts orders, fetches live price from catalog-service, and calculates totals |

## 📁 Project Structure


shopping_cart/

├── catalog-service/
│ ├── app code
│ ├── Dockerfile
│ └── requirements.txt
│
├── order-service/
│ ├── app code
│ ├── Dockerfile
│ └── requirements.txt
│
├── frontend-service/
│ ├── app code
│ ├── Dockerfile
│ └── requirements.txt
│
├── k8s/
│ ├── 00-namespaces.yaml
│ ├── 01-catalog-service.yaml
│ ├── 02-order-service.yaml
│ ├── 03-frontend-service.yaml
│ └── 04-configmap.yaml
│
└── Jenkinsfile

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Application | Python, Microservices Architecture |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | Jenkins |
| Source Control | GitHub |
| Configuration Management | Kubernetes ConfigMap |
| Environment |  Linux |


