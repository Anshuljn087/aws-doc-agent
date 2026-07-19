# S3 versioning

S3 versioning is a feature that keeps multiple versions of an object in the same bucket. When versioning is enabled, every time a new upload replaces an existing object, AWS preserves the previous version instead of overwriting it. This makes versioning useful for recovery, auditing, and change tracking.

Versioning is especially important when data is edited frequently. For example, if a file is updated accidentally, an earlier version can be restored from the bucket. Versioning does not automatically delete old versions, so storage costs can increase over time unless lifecycle rules are configured.

There are two common management practices with versioned buckets. First, teams often use lifecycle policies to expire old versions after a retention period. Second, they may enable MFA Delete for additional protection against accidental or unauthorized deletion. MFA Delete requires multi-factor authentication for certain delete operations.

Versioning is independent of object encryption. A versioned object can still be encrypted with SSE-S3, SSE-KMS, or client-side encryption. It is also worth noting that versioning must be enabled at the bucket level and remains enabled until it is suspended. If a bucket is later suspended, existing versions remain available unless they are explicitly deleted.

To enable versioning in the AWS console, open the target S3 bucket, choose Properties, find Bucket versioning, select Edit, enable Versioning, and save the change. With the AWS CLI, the equivalent command is `aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled`. After versioning is enabled, uploading a new version of an object preserves the previous version instead of replacing it. You can later restore an earlier version from the object’s version list, and you can use lifecycle rules to expire older versions when retention is no longer needed.
