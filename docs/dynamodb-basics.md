# Amazon DynamoDB basics

Amazon DynamoDB is AWS's fully managed NoSQL database service. It is designed for applications that need low-latency reads and writes at any scale. DynamoDB stores data in tables, and each item is a set of attributes that can be queried using primary keys and secondary indexes.

A key strength of DynamoDB is its ability to scale horizontally with predictable performance. It supports both on-demand and provisioned capacity modes, which lets teams choose between flexible scaling and cost control. The service also provides features such as encryption at rest, point-in-time recovery, and automatic backups.

DynamoDB is commonly used for session storage, user profiles, application state, and event-driven workloads. Its simple data model makes it a strong fit for applications that need fast access to key-value or document-style data. Many developers also use it together with Lambda to create responsive event-driven applications.

When designing a DynamoDB table, developers usually think carefully about partition keys and access patterns. A well-chosen key structure can improve performance and reduce hot partitions, which helps the application remain efficient as traffic grows.
