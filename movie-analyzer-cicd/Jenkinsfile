pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  restartPolicy: Never

  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.23.2-debug
    command: ["/busybox/sh", "-c"]
    args: ["sleep infinity"]
    tty: true
    volumeMounts:
    - name: workspace
      mountPath: /home/jenkins/agent

  - name: helm
    image: dtzar/helm-kubectl:3.14.0
    command: ["cat"]
    tty: true
    volumeMounts:
    - name: workspace
      mountPath: /home/jenkins/agent

  - name: jnlp
    image: jenkins/inbound-agent:3345.v03dee9b_f88fc-1
    args: ["\$(JENKINS_SECRET)", "\$(JENKINS_NAME)"]
    volumeMounts:
    - name: workspace
      mountPath: /home/jenkins/agent

  volumes:
  - name: workspace
    emptyDir: {}
"""
    }
  }

  environment {
    AWS_REGION   = "ap-south-1"
    ECR_ACCOUNT = "433193941125"
    ECR_REGISTRY = "${ECR_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    TAG = "${BUILD_NUMBER}"
  }

  stages {

    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Build & Push Images") {
      steps {
        container("kaniko") {
          sh """
echo "🚀 Building Backend"
/kaniko/executor \
  --context=dir://${WORKSPACE}/backend \
  --dockerfile=${WORKSPACE}/backend/Dockerfile \
  --destination=${ECR_REGISTRY}/movie-backend:${TAG} \
  --verbosity=info

echo "🚀 Building Frontend"
/kaniko/executor \
  --context=dir://${WORKSPACE}/frontend \
  --dockerfile=${WORKSPACE}/frontend/Dockerfile \
  --destination=${ECR_REGISTRY}/movie-frontend:${TAG} \
  --verbosity=info

echo "🚀 Building Model"
/kaniko/executor \
  --context=dir://${WORKSPACE}/model \
  --dockerfile=${WORKSPACE}/model/Dockerfile \
  --destination=${ECR_REGISTRY}/movie-model:${TAG} \
  --verbosity=info
"""
        }
      }
    }

    stage('Deploy to Kubernetes using Helm') {
  steps {
    container('helm') {
      sh '''
        echo "📥 Cloning Helm repo"
        rm -rf movie-analyzer-helm
        git clone https://github.com/DeviVaraPrasadJ-dev/movie-analyzer-helm.git

        echo "🚀 Deploying movie-analyzer using Helm"

        helm upgrade --install movie-analyzer ./movie-analyzer-helm \
          --namespace movie-analyzer \
          --create-namespace \
          --values movie-analyzer-helm/values-dev.yaml \
          --set backend.image.repository=${ECR_REGISTRY}/movie-backend \
          --set backend.image.tag=${BUILD_NUMBER} \
          --set frontend.image.repository=${ECR_REGISTRY}/movie-frontend \
          --set frontend.image.tag=${BUILD_NUMBER} \
          --set model.image.repository=${ECR_REGISTRY}/movie-model \
          --set model.image.tag=${BUILD_NUMBER}

        echo "✅ Helm deployment completed"
      '''
    }
  }
}
  }

  post {
    success {
      echo "✅ Backend, Frontend & Model images pushed to ECR"
    }
    failure {
      echo "❌ Pipeline failed"
    }
  }
}
