# Amazon Bedrock Knowledge Bases

Amazon Bedrock Knowledge Bases provide a managed way to connect foundation models to your own documents and data. They allow you to create retrieval-augmented generation, or RAG, applications that answer questions using relevant content from a curated knowledge source rather than relying only on model training data. This is especially useful for domain-specific documentation and internal knowledge.

A Knowledge Base typically combines a vector store, document ingestion, and retrieval orchestration. Documents are ingested, chunked, and embedded so a model can retrieve the most relevant passages during a query. The retrieved passages are then passed to a model as context, which helps produce grounded answers.

Bedrock Knowledge Bases support integration with Amazon OpenSearch Service Serverless and other supported vector databases. They can be used with foundation models available in Amazon Bedrock, including models from Anthropic, Meta, and Amazon. The pattern is well suited for chatbots, support assistants, and enterprise search experiences.

For a demo application, a Knowledge Base is a practical way to ground answers in a specific documentation set. It reduces hallucinations and allows the system to answer questions about a controlled corpus of content with more consistency.
