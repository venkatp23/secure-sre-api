# 1. Define the Provider (Who are we talking to?)
provider "aws" {
  region = "us-east-1"
}

# 2. Create the "Hardened" S3 Bucket (Rank 2: SRE)
resource "aws_s3_bucket" "app_logs" {
  bucket = "secure-sre-logs-${random_id.suffix.hex}" # Unique name
  force_destroy = true # Helps in deleting the bucket by force even if it have files and versioning
}

# 3. Enable Versioning (Rank 2: SRE - Reliability)
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.app_logs.id
  versioning_configuration {
    status = "Enabled" # Allows us to "Roll back" if data is accidentally deleted
  }
}

# 4. Block Public Access (Rank 1: Cyber Security)
resource "aws_s3_bucket_public_access_block" "security_gate" {
  bucket = aws_s3_bucket.app_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true # Prevents data leaks!
}

# Helper to make the bucket name unique
resource "random_id" "suffix" {
  byte_length = 4
}