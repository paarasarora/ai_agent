#!/bin/bash

AWS_REGION='us-east-1'
ECR_REPO_URL="766197614255.dkr.ecr.us-east-1.amazonaws.com/ai-agent"

# Log in to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URL

# Build and push Docker image
echo "Building and pushing Docker image..."
docker build -t $ECR_REPO_URL:latest ../
docker push $ECR_REPO_URL:latest

# Force new deployment
echo "Forcing new deployment of ECS service..."
aws ecs update-service --cluster ai-agent-cluster --service ai-agent-service --force-new-deployment --region $AWS_REGION

echo "Deployment complete!"