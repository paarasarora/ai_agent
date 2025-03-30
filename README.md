# 🚀 **AI Agent Application**

## 📝 **Overview**
The **AI Agent Application** simulates conversations between **ChatGPT-powered AI agents** about food preferences. It is built using **Django** and **Django REST Framework (DRF)**, with **OpenAI** integration for natural language processing. The application is deployed on **AWS infrastructure** using **ECS Fargate** with automated provisioning through **Terraform**.

### 🌐 **Live Demo**
[AI Agent Application](http://ai-agent-alb-13659448.us-east-1.elb.amazonaws.com/)

---

## 🎯 **Features**
✅ Simulate conversations between two ChatGPT-powered agents  
✅ Generate and store food preferences dynamically  
✅ Interactive chat interface for real-time conversation  
✅ API endpoints for conversation management  
✅ Authentication using token-based authentication  
✅ View conversation history and food preferences  
✅ User management with login, account management, and user creation  

---

## ⚙️ **Architecture**


The application is deployed on **AWS** with the following components:

### 🔥 **Frontend**
- **Static files** (CSS, JavaScript, and HTML) are served via **Amazon S3**, providing a **scalable and cost-effective** static file hosting solution.
  
### 🛠️ **Backend**
- The **Django application** is containerized using **Docker** and runs on **AWS ECS Fargate**, which provides serverless container orchestration.
- ECS tasks are automatically scaled using **AWS Auto Scaling**.
- FoodieBot's project application is **food_chat**, mentioning it for more clarity.

### 🛢️ **Database**
- **PostgreSQL** database hosted on **Amazon RDS**.
- RDS ensures data persistence, backups, and easy scaling.

### ⚖️ **Load Balancer**
- An **AWS Application Load Balancer (ALB)** distributes incoming traffic to ECS Fargate services.
- The ALB ensures **high availability** and handles incoming requests efficiently.

### 🛡️ **Security**
- **IAM roles and policies** manage access to AWS resources securely.
- **AWS Parameter Store** is used to store sensitive information like API keys and database credentials securely.
- **Security Groups** control access at the **network level**.

### 🔍 **Monitoring & Logging**
- **Amazon CloudWatch** is used for collecting and monitoring application logs and ECS task metrics.
- Logs include conversation data, errors, and other application activities.

### 📦 **Container Registry**
- **Amazon Elastic Container Registry (ECR)** is used for storing Docker images.
- The CI/CD pipeline pushes new images to ECR during deployment.

---

## 🔥 **API Endpoints**

### 🗨️ **Conversation Endpoints**

| **Endpoint**                  | **Method** | **Description**                        | **Authentication**         |
|-------------------------------|-----------|----------------------------------------|----------------------------|
| `/`| POST      | Conversation history, this is the landing page | None    |
| `/chat/invoke/`                | POST      | Start a new conversation              | None                       |
| `/start/`      | POST      | Used internally inside the template    | None                       |
| `/generate/`                     | GET       | Simulate conversation between 2 chatgpt's                 | Token Authentication               |

** bash ```/generate/``` endpoint expects count as the parameter to control the number of iterations **

### 👤 **User Endpoints**

| **Endpoint**        | **Method** | **Description**               | **Authentication**         |
|---------------------|-----------|--------------------------------|----------------------------|
| `/users/create-users/` | POST      | Create a new user               | None                       |
| `/users/my-account/`    | GET       | Get details of current user     | Token Authentication       |
| `/users/login/`         | POST      | Log in as an existing user      | Token Authentication       |

---

## 📊 **Views**

- **Conversations List:** View all conversations.  
- **Chat Interface:** Interactive chat with AI agents.  
- **Conversation History:** View the full history of conversations, including food preferences.  
- **User Management:** Create users, log in, and manage accounts.  

---

## 🚀 **Deployment Instructions**

The **AI Agent Application** only supports deployment to **production** using a **Bash script** located in the `infra` folder.

### ✅ **Prerequisites**
Ensure you have the following installed:
- **AWS CLI** (configured with proper credentials)
- **Docker**
- **Terraform**
- **.env file** (please reach out to me for access)

### ✅ **Deployment Steps**

1. **Navigate to the `infra` folder:**
   ```bash
   cd infra

2. ✅ **Run the deployment script:**

```bash
bash deployment.sh
```
The deployment.sh script will:

🚀 Build and push the Docker image to ECR

🚀 Deploy the image to ECS Fargate

🚀 Apply the infrastructure configuration using Terraform








