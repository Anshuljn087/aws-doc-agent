# Amazon VPC basics

Amazon Virtual Private Cloud, or VPC, lets users create an isolated network inside AWS. A VPC gives you control over IP address ranges, subnets, route tables, gateways, and network access controls. This makes it possible to design private, logically isolated environments for applications and services.

A VPC is usually divided into public and private subnets. Public subnets can route traffic directly to the internet through an Internet Gateway, while private subnets are intended for internal resources that should not be directly exposed. Security groups and network access control lists provide layer-based filtering for inbound and outbound traffic.

VPCs support connectivity options such as Internet Gateway, NAT Gateway, Virtual Private Gateway, and VPC peering. These features allow workloads to communicate with the internet, with on-premises networks, or with other VPCs. Proper VPC design is crucial for security, performance, and maintainability.

When building AWS applications, a well-planned VPC helps separate tiers of an application and limits exposure to the internet. This is especially important for databases, internal services, and systems that require strict access control.
