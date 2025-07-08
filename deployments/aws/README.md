# AWS Deployment Configuration

This directory contains example configurations for deploying the application to AWS using ECS with Fargate.

### Files:

- `buildspec.yml`: This file is used by AWS CodeBuild to build the Docker images and push them to Amazon ECR (Elastic Container Registry).

- `task-definitions/`: This directory contains the ECS task definition templates.
  - `backend-task-def.json`: Task definition for the backend service.
  - `frontend-task-def.json`: Task definition for the frontend service.

### Deployment Steps:

1.  **Create ECR Repositories**: Create two ECR repositories, one for the backend and one for the frontend.
2.  **Set up CodeBuild**: Create a CodeBuild project linked to your source code repository. Use the `buildspec.yml` in this directory as the build specification.
3.  **Create ECS Cluster**: Create an ECS cluster to run your services.
4.  **Create Task Definitions**: Register new task definitions in ECS using the JSON files in the `task-definitions` directory. You will need to replace the placeholder values (like `YOUR_ECR_REPO_URI`) with your actual ECR repository URIs.
5.  **Create ECS Services**: Create two services in your ECS cluster, one for the frontend and one for the backend, using the task definitions you just created. Configure them with a load balancer to expose them to the internet.
