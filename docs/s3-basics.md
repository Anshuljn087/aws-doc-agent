# Amazon S3 basics

Amazon Simple Storage Service, or S3, is AWS's object storage service for storing and retrieving any amount of data. It is commonly used for backups, media files, logs, and static website assets. S3 stores data as objects inside buckets, and each object is identified by a unique key. Buckets are the top-level containers, and a single bucket can hold millions of objects.

A key design feature of S3 is durability. AWS replicates data across multiple Availability Zones to provide high durability for stored objects. S3 also offers different storage classes such as Standard, Intelligent-Tiering, Standard-IA, and Glacier. These classes differ in cost and access speed, so teams can choose based on how often data is accessed.

S3 supports access control through bucket policies and IAM permissions. Users can make buckets private, public, or shared with specific principals. S3 also integrates with features like event notifications, lifecycle rules, and versioning. Lifecycle rules can automatically move objects between storage classes or delete them after a set period.

For developers, S3 is often the default choice for file storage because it is simple to use and highly scalable. A typical workflow includes uploading files with the AWS CLI, SDKs, or the console, then granting access to applications that need to read or write those files.
