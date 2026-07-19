# Amazon EC2 basics

Amazon Elastic Compute Cloud, or EC2, provides resizable virtual servers in the cloud. These virtual machines, often called instances, can be launched in minutes and used for web servers, application hosting, batch processing, and testing. EC2 is one of the foundational services in AWS because it provides flexible compute capacity.

EC2 instances run on virtual hardware and can be selected based on CPU, memory, storage, and networking needs. AWS offers a variety of instance families, including general purpose, compute optimized, memory optimized, and accelerated computing options. This flexibility allows organizations to choose the best fit for their workload.

Each EC2 instance is associated with an Amazon Machine Image, or AMI, which defines the operating system and software configuration. Users can launch instances from a public AMI, a custom AMI, or a marketplace image. Security groups and IAM roles are often used alongside instances to control inbound traffic and permissions.

EC2 is a core building block for many AWS architectures. Developers often use it when they need direct operating system access or want to run applications that do not fit well into a serverless model.
