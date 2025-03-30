# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy to"
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project"
  default     = "ai-agent"
}

variable "environment" {
  description = "The deployment environment"
  default     = "production"
}

variable "container_port" {
  description = "Port exposed by the Docker container"
  default     = 8000
}

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/health/"
}

variable "container_cpu" {
  description = "The number of cpu units to reserve for the container"
  default     = "512" # 0.5 vCPU 
}

variable "container_memory" {
  description = "The amount of memory to reserve for the container"
  default     = "1024" # 1 GB
}

variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 1
}

variable "db_instance_class" {
  description = "The RDS instance class"
  default     = "db.t3.micro"
}

variable "db_username" {
  description = "Username for the RDS PostgreSQL instance"
  default     = "dbadmin"
}

variable "db_password" {
  description = "Password for the RDS PostgreSQL instance"
  sensitive   = true
}

variable "db_name" {
  description = "The name of the database"
  default     = "agentdb"
}

variable "env_file_path" {
  description = "Path to the .env file"
  default     = "/mnt/c/Users/paara/OneDrive/Documents/GitHub/ai_agent/.env"
}

# locals.tf

locals {
  # Read the .env file and convert it to a map
  env_file_content = fileexists(var.env_file_path) ? file(var.env_file_path) : ""

  env_vars = {
    for line in compact(split("\n", local.env_file_content)) :
    trimspace(split("=", line)[0]) => trimspace(join("=", slice(split("=", line), 1, length(split("=", line)))))
    if length(split("=", line)) > 1 && !startswith(trimspace(line), "#")
  }
}