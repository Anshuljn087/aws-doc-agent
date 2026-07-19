output "docs_bucket_name" {
  value = aws_s3_bucket.docs.bucket
}

output "bedrock_role_arn" {
  value = aws_iam_role.bedrock_kb_access.arn
}
