# 🍽️ FoodieBot

FoodieBot is a Django-based chatbot application designed to discuss food preferences, recipes, and culinary topics with users. It leverages OpenAI's models for natural conversations and is deployed on AWS using Terraform-managed infrastructure.

## Overview

FoodieBot enables users to:
- Discuss their favorite foods
- Track food preferences and dietary restrictions
- Engage in natural conversations about culinary topics
- Store conversation history for future reference

## Architecture

### Infrastructure as Code

FoodieBot's infrastructure is fully defined and managed using Terraform, enabling consistent, reproducible deployments and infrastructure versioning.

### Cloud Infrastructure

The application is deployed on AWS with a modern microservices architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  AWS ALB    │────▶│  ECS Fargate │
│   Browser   │     │  (Load      │     │  Container   │
└─────────────┘     │  Balancer)  │     │  Service     │
                    └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  OpenAI API │◀───▶│  Django App │
                    │             │     │             │
                    └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ PostgreSQL  │
                                        │ RDS Database│
                                        └─────────────┘
```

### AWS Components

| Component | Description |
|-----------|-------------|
| **VPC** | Custom VPC with public and private subnets across 2 AZs |
| **ECS Fargate** | Serverless container orchestration for the Django application |
| **Application Load Balancer** | Distributes incoming traffic across containers |
| **RDS PostgreSQL** | Managed database service for data persistence |
| **ECR** | Container registry for Docker images |
| **CloudWatch** | Monitoring and logging solution |
| **IAM Roles** | Task execution roles with principle of least privilege |
| **Auto Scaling** | CPU-based scaling policies to handle load variations |
| **SSM Parameter Store** | Secure storage for environment variables and secrets |

### Security Features

- Private subnets for application containers and database
- Security groups with principle of least access
- Secrets management via AWS SSM Parameter Store
- Database credentials stored as secure strings
- HTTPS support via ALB (configurable)

## Tech Stack

- **Backend**: Django with Django REST Framework
- **AI Integration**: OpenAI API (GPT-3.5 Turbo & GPT-4o Mini)
- **Database**: PostgreSQL on AWS RDS
- **Container Orchestration**: AWS ECS Fargate
- **Infrastructure as Code**: Terraform
- **CI/CD**: Deployment scripts for automated updates

## Terraform Components

The Terraform configuration includes:

### Network Resources
- VPC with public and private subnets
- NAT Gateway for outbound internet access
- Route tables and security groups

### Compute Resources
- ECS Cluster and Service definitions
- Task definitions with container configurations
- Auto-scaling policies based on CPU utilization

### Database Resources
- RDS PostgreSQL instance
- DB subnet groups and parameter groups
- Security groups for database access

### Security and IAM
- Task execution roles for ECS
- IAM policies for SSM Parameter Store access
- Security groups with least privilege access

## Deployment Scripts

FoodieBot uses two key scripts to manage infrastructure deployment and application updates:

### setup.sh

The `setup.sh` script provides a comprehensive setup process for the entire infrastructure:

```bash
cd infra
bash setup.sh
```

Key functionality:
- Verifies prerequisites (Terraform, AWS CLI, Docker)
- Validates AWS configuration and credentials
- Creates a `terraform.tfvars` file with project configuration
- Generates a random secure password for the database
- Initializes Terraform (`terraform init`)
- Plans the deployment (`terraform plan`)
- Prompts for confirmation before proceeding
- Applies the Terraform configuration (`terraform apply`)
- Retrieves the ECR repository URL from Terraform outputs
- Logs in to ECR using AWS credentials
- Builds and pushes the Docker image to ECR
- Forces a new deployment on the ECS service

Key checks performed:
1. Verifies `.env` file exists with required environment variables
2. Confirms required tools are installed (terraform, aws-cli, docker)
3. Validates AWS CLI configuration
4. Confirms AWS account ID is accessible

### deployment.sh

The `deployment.sh` script handles application updates without modifying the underlying infrastructure:

```bash
cd infra
bash deployment.sh
```

Key functionality:
- Logs in to ECR with current AWS credentials
- Builds a new Docker image from the application code
- Tags and pushes the image to the ECR repository
- Forces ECS service to deploy the new container version

This provides a streamlined workflow for deploying code changes after the infrastructure is established. The script is straightforward but powerful, enabling continuous delivery of application updates.

Example usage:
```bash
# After making code changes to the application
cd infra
bash deployment.sh
```

## Environment Configuration

Create a `.env` file with the following variables:

```
OPEN_AI_KEY=your_openai_api_key
DEBUG=False
SECRET_KEY=your_django_secret_key
```

These values will be securely stored in AWS SSM Parameter Store during deployment.

## Application Features

### User Conversations
- Users can have real-time conversations with FoodieBot
- Food preferences are extracted and stored during conversations
- Conversation history is saved for future reference

### Food Preference Analysis
- Automatic detection of vegetarian and vegan preferences
- Ranking of favorite foods
- Storage of food preferences for personalized interactions

### API Endpoints
- `/chat/invoke` - Main chat interface
- `/start/` - Start a new conversation
- `/message/` - Send a message to the bot
- `/history/<id>/` - View conversation history
- `/generate/` - Generate simulated conversations (admin only)
- `/health/` - Health check endpoint

## Local Development

1. **Clone the repository**

2. **Set up environment variables**
   Create a `.env` file in the root directory.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## Infrastructure Customization

You can customize the infrastructure by modifying the following files:

- `infra/variables.tf` - Infrastructure configuration options
- `infra/main.tf` - Main Terraform configuration
- `infra/setup.sh` - Deployment automation script

Key configurable parameters include:
- AWS region
- Container resources (CPU/memory)
- Database instance type
- Auto-scaling parameters
- Health check paths

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
