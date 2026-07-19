# AWS Documentation RAG Chatbot

This project is a Retrieval-Augmented Generation (RAG) chatbot for exploring AWS documentation through a chat interface. It combines a FastAPI backend, a Bedrock-backed retrieval flow, and a React UI, and can be run entirely locally or deployed to AWS (EC2 backend + S3-hosted frontend).

## What this demo does

- Serves a chat experience for asking AWS questions in plain English.
- Retrieves relevant documentation from an Amazon Bedrock Knowledge Base.
- Generates grounded answers using Amazon Bedrock models.
- Rewrites follow-up questions into standalone queries using conversation history.
- Falls back to bundled local Markdown docs if the Knowledge Base is unavailable.
- Caches recent answers in-memory to reduce repeat Bedrock calls.

## Architecture overview

- The documentation corpus lives in [docs](docs) as short, focused Markdown files covering core AWS services.
- The Python service in [agent.py](agent.py) handles query reformulation, retrieval, local-doc fallback, generation, and caching.
- The FastAPI app in [app.py](app.py) exposes `/chat`, `/health`, and `/cache-stats` endpoints.
- The Vite + React interface in [frontend](frontend) provides the conversational UI and talks to the backend over `VITE_API_BASE_URL`.
- [infra](infra) contains Terraform for the EC2 instance that hosts the backend (security group, IAM role scoped to `bedrock:InvokeModel`/`bedrock:Retrieve`, and the instance itself). The docs S3 bucket and the Bedrock Knowledge Base are created manually (console/CLI), not by this Terraform config — see Design decisions below.

## Local setup

1. Configure AWS credentials:
   - Run `aws configure`
   - Ensure your account can access Amazon Bedrock and the Knowledge Base APIs.
2. Create a Bedrock Knowledge Base in the AWS console:
   - Open the Amazon Bedrock console.
   - Create a Knowledge Base and connect it to an S3 bucket containing the documentation files (upload the contents of [docs](docs)).
   - Ingest the documents and note the Knowledge Base ID.
3. Set the environment values in [.env](.env) (not committed to git):
   ```
   KB_ID=<your-knowledge-base-id>
   AWS_REGION=<your-region>
   MODEL_ID=<optional-inference-profile-id-or-arn>
   ```
4. Start the backend:
   - `pip install -r requirements.txt`
   - `uvicorn app:app --reload --port 8000`
5. Start the frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Deploying to AWS

**Backend (EC2, via Terraform):**
```
cd infra
terraform init
terraform apply
```
This provisions a `t3.micro` instance whose boot script installs dependencies, clones this repo, and runs the FastAPI app as a systemd service. The public IP is printed as the `backend_public_ip` output.

**Frontend (S3 static website):**
```
cd frontend
$env:VITE_API_BASE_URL = "http://<backend_public_ip>:8000"
npm run build
aws s3 sync dist/ s3://<your-frontend-bucket>/ --delete
```
The bucket needs static website hosting enabled and a public-read bucket policy — see the bucket's own setup for the one-time configuration.

## Design decisions

The Knowledge Base and its S3 docs bucket are created via the AWS console/CLI rather than Terraform, because that remains the more practical path for KB creation and document ingestion today. Terraform is scoped to the part that benefits most from being reproducible: the EC2 compute layer running the backend.

For production, the next steps would be containerizing the service and deploying through ECS (or similar) instead of a single EC2 instance, adding HTTPS via CloudFront + ACM, managing secrets more securely (e.g. Secrets Manager instead of a plain `.env`), and automating Knowledge Base ingestion/sync as part of the deployment pipeline.
