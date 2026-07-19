variable "aws_region" {
  description = "AWS region for the demo resources"
  type        = string
  default     = "us-east-1"
}

variable "docs_bucket_name" {
  description = "Name of the S3 bucket that will host the documentation files"
  type        = string
  default     = "aws-doc-agent-demo-docs"
}

variable "bedrock_role_name" {
  description = "IAM role name for Bedrock Knowledge Base access"
  type        = string
  default     = "bedrock-kb-access-demo"
}

variable "github_repo_url" {
  description = "GitHub URL of this repo, cloned onto the EC2 instance at boot"
  type        = string
  default     = "https://github.com/Anshuljn087/aws-doc-agent.git"
}

variable "kb_id" {
  description = "Bedrock Knowledge Base ID used by the FastAPI backend"
  type        = string
  default     = "AQJ8REZKK9"
}
