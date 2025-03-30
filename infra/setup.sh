#!/bin/bash
# setup.sh - Script to deploy Django application to AWS Fargate using Terraform

set -e

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found"
  exit 1
fi

# Check required tools
command -v terraform >/dev/null 2>&1 || { echo "Error: terraform is required but not installed"; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "Error: aws-cli is required but not installed"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Error: docker is required but not installed"; exit 1; }

# Check AWS CLI configuration
echo "Checking AWS configuration..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ $? -ne 0 ]; then
  echo "Error: AWS CLI not configured properly. Run 'aws configure' first."
  exit 1
fi

echo "AWS Account ID: $AWS_ACCOUNT_ID"
AWS_REGION=$'us-east-1'
echo "AWS Region: $AWS_REGION"

echo "AWS Account ID: $AWS_ACCOUNT_ID"

# Create a terraform.tfvars file
echo "Creating terraform.tfvars file..."
DB_PASSWORD=$(openssl rand -base64 16 | tr -d '/+=' | cut -c1-16)

cat > terraform.tfvars <<EOF
aws_region = "$AWS_REGION"
project_name = "ai-agent"
environment = "production"
db_password = "$DB_PASSWORD"
env_file_path = "./.env"
EOF

# Initialize Terraform
echo "Initializing Terraform..."
terraform init

# Plan the deployment
echo "Planning Terraform deployment..."
terraform plan -out=tfplan

# Ask for confirmation
read -p "Do you want to proceed with the deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Deployment cancelled."
  exit 0
fi

# Apply Terraform plan
echo "Applying Terraform deployment..."
terraform apply tfplan

# Get ECR repository URL
ECR_REPO_URL=$(terraform output -raw ecr_repository_url)
if [ -z "$ECR_REPO_URL" ]; then
  echo "Error: Could not get ECR repository URL from Terraform output"
  exit 1
fi

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
