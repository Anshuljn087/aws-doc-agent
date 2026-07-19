data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "backend" {
  name        = "aws-doc-agent-backend-sg"
  description = "Allow SSH and FastAPI access to the aws-doc-agent backend"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "FastAPI backend"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "aws-doc-agent-backend-sg"
  }
}

resource "aws_iam_role" "ec2_bedrock_access" {
  name = "aws-doc-agent-ec2-bedrock-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "ec2_bedrock_access" {
  name = "bedrock-invoke-retrieve"
  role = aws_iam_role.ec2_bedrock_access.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "BedrockInvokeAndRetrieve"
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:Retrieve"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_bedrock_access" {
  name = "aws-doc-agent-ec2-bedrock-access"
  role = aws_iam_role.ec2_bedrock_access.name
}

resource "aws_key_pair" "backend" {
  key_name   = "aws-doc-agent-backend-key"
  public_key = file(pathexpand(var.ssh_public_key_path))
}

resource "aws_instance" "backend" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = "t3.micro"
  subnet_id              = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.backend.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_bedrock_access.name
  key_name               = aws_key_pair.backend.key_name

  user_data = <<EOF
#!/bin/bash
set -euxo pipefail

dnf install -y python3.11 python3.11-pip git

git clone ${var.github_repo_url} /opt/aws-doc-agent
cd /opt/aws-doc-agent

python3.11 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

cat > /opt/aws-doc-agent/.env <<ENVEOF
KB_ID=${var.kb_id}
AWS_REGION=${var.aws_region}
MODEL_ID=${var.model_id}
ENVEOF

cat > /etc/systemd/system/aws-doc-agent.service <<'UNITEOF'
[Unit]
Description=AWS Doc Agent FastAPI backend
After=network.target

[Service]
WorkingDirectory=/opt/aws-doc-agent
ExecStart=/opt/aws-doc-agent/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
User=root

[Install]
WantedBy=multi-user.target
UNITEOF

systemctl daemon-reload
systemctl enable aws-doc-agent
systemctl start aws-doc-agent
EOF

  tags = {
    Name = "aws-doc-agent-backend"
  }
}
