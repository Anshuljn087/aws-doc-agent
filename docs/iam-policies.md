# IAM policies

IAM policies are JSON documents that define permissions in AWS. They specify which actions are allowed or denied on which resources and under what conditions. Policies can be attached to users, groups, roles, and other identities, making them the core mechanism for authorization in AWS.

There are two main policy types: identity-based policies and resource-based policies. Identity-based policies are attached to an IAM principal and control what that identity can do. Resource-based policies are attached directly to a resource such as an S3 bucket or an SNS topic and define which principals can access it.

AWS supports both allow and deny statements. In general, explicit deny statements take precedence over allow statements. This makes it possible to enforce stricter restrictions even when broader permissions are granted elsewhere. Policies should be written carefully to follow least-privilege principles and avoid overly broad wildcards.

A common practice is to create policies that grant only the specific API actions required by an application. For example, a Lambda execution role might need permission to write logs and read from a specific S3 bucket, but not to manage all AWS resources. Well-scoped policies reduce security risk and make auditing easier.
