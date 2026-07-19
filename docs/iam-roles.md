# IAM roles

AWS Identity and Access Management, or IAM, is the service used to control who can access AWS resources and what they can do. IAM roles are one of the most important concepts in AWS security. A role is an identity that grants permissions to trusted principals, such as users, applications, or other AWS services, without requiring long-term credentials.

Roles are often used for service-to-service access. For example, an EC2 instance can assume an IAM role so it can read data from an S3 bucket or call a DynamoDB table. A Lambda function can also assume a role to access other AWS resources securely. This design is preferred over embedding access keys directly in code.

A role contains a trust policy that defines which principals are allowed to assume it and an attached permissions policy that defines what actions are permitted. This separation makes it easier to follow least-privilege access principles. When a service assumes a role, AWS temporarily provides short-lived credentials for the session.

Using IAM roles improves security and simplifies access management. They are especially valuable in automated environments where applications need dynamic credentials without manual rotation or secret storage.
