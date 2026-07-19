# AWS Documentation RAG Chatbot

This project is a polished local demo for exploring AWS documentation through a chat interface. It combines a lightweight FastAPI backend, a Bedrock-backed retrieval flow, and a refined React UI so the experience feels closer to a thoughtfully built product prototype than a quick script.

## What this demo does

- Serves a local chat experience for asking AWS questions in plain English.
- Retrieves relevant documentation from an Amazon Bedrock Knowledge Base.
- Generates grounded answers using Amazon Bedrock models.
- Keeps the implementation local and demo-friendly without using Lambda.

## Architecture overview

- The documentation corpus lives in [docs](docs) as short, focused Markdown files covering core AWS services.
- The Python service in [agent.py](agent.py) handles retrieval and answer generation.
- The FastAPI app in [app.py](app.py) exposes a simple /chat endpoint for the UI.
- The Vite + React interface in [frontend](frontend) provides a clean, conversational experience for testing the workflow.

## Setup

1. Configure AWS credentials:
   - Run `aws configure`
   - Ensure your account can access Amazon Bedrock and the Knowledge Base APIs.
2. Create the Terraform resources:
   - `cd infra`
   - `terraform init`
   - `terraform apply`
3. Create a Bedrock Knowledge Base in the AWS console:
   - Open the Amazon Bedrock console.
   - Create a Knowledge Base and connect it to an S3 bucket containing the documentation files.
   - Ingest the documents and note the Knowledge Base ID.
4. Set the environment values:
   - Windows PowerShell: `$env:KB_ID="<your-knowledge-base-id>"`
   - Optional: `$env:MODEL_ID="<your-inference-profile-id-or-arn>"`
   - Or store them in [.env](.env) for local development.
5. Start the backend:
   - `uvicorn app:app --reload --port 8000`
6. Start the frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Design decisions

The Knowledge Base is created in the AWS console for this demo because it is the fastest path to a working proof of concept and it makes the workflow easier to understand during a short-lived evaluation. Terraform is still included for the supporting infrastructure, but the Bedrock Knowledge Base creation and ingestion experience remains more practical through the console at this stage.

For production, the next step would be to containerize the service, deploy it through ECS or a similar platform, manage secrets more securely, and automate Knowledge Base ingestion and sync as part of the deployment pipeline.
