provider "aws" {
  region = "us-east-1"
}

# 1. S3 BUCKET: Publicly Accessible & Unencrypted
# JD Goal: Automate IaC scanning to find misconfigurations
resource "aws_s3_bucket" "data_leak" {
  bucket = "company-confidential-backups-99"
}

resource "aws_s3_bucket_public_access_block" "allow_public" {
  bucket = aws_s3_bucket.data_leak.id

  # VULNERABILITY: Setting these to false allows public access
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 2. IAM POLICY: Overly Permissive (Star (*) Permission)
# JD Goal: Production environment security & CNAPP monitoring
resource "aws_iam_policy" "admin_access" {
  name        = "over-permissive-policy"
  description = "Allows all actions on all resources"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "*"
        Effect   = "Allow"
        Resource = "*" # VULNERABILITY: This is a massive security risk
      },
    ]
  })
}

# 3. SECURITY GROUP: Open to the World
# JD Goal: Monitor for new misconfiguration security issues
resource "aws_security_group" "open_ssh" {
  name        = "allow_all_ssh"
  description = "Allow SSH from anywhere"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # VULNERABILITY: Should never allow 0.0.0.0/0 for SSH
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 4. EBS VOLUME: Not Encrypted at Rest
resource "aws_ebs_volume" "unencrypted_vol" {
  availability_zone = "us-east-1a"
  size              = 10
  # VULNERABILITY: Encryption is disabled
  encrypted         = false 
}