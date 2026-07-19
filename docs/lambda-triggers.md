# Lambda triggers

Lambda functions can be triggered by a wide range of AWS services, making them a central component in event-driven architectures. For example, S3 can invoke a Lambda function when an object is created or deleted. DynamoDB streams can trigger a function when records change, which is useful for replication or downstream processing workflows.

API Gateway is a common trigger for web or mobile applications. When an HTTP request reaches API Gateway, it can forward the request to a Lambda function that returns a response. EventBridge can also route events to Lambda, enabling loosely coupled integrations across multiple AWS services.

Another common pattern is scheduled execution with EventBridge Scheduler or CloudWatch Events. This allows functions to run on a fixed cron or rate schedule for operational tasks such as cleanup, reporting, or maintenance. In addition, SNS and SQS can be used to fan out messages to Lambda workers.

The main idea behind Lambda triggers is that the function responds to the event rather than waiting for a constant server to be running. This makes it easier to build responsive systems that scale automatically and only consume resources when needed.
