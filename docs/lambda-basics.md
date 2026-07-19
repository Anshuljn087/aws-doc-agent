# AWS Lambda basics

AWS Lambda is a serverless compute service that runs code in response to events without requiring users to manage servers. Developers upload code as a function, define its runtime and memory, and AWS handles the execution environment. Lambda is commonly used for data processing, automation, event-driven workflows, and API backends.

A Lambda function is triggered by events from services such as S3, DynamoDB, EventBridge, API Gateway, or schedules. When an event occurs, Lambda executes the function asynchronously or synchronously depending on the integration pattern. AWS automatically scales based on the number of incoming requests, which makes Lambda well suited for burst workloads.

Lambda functions are billed based on the number of requests and the duration of code execution. This can be cost-effective for intermittent workloads because there is no charge when the function is idle. However, function code should be designed to stay efficient and avoid long-running operations that could increase cost.

Common Lambda use cases include image processing, file validation, stream processing, and webhook handlers. When building with Lambda, developers usually keep functions small, stateless, and focused on a single responsibility.
