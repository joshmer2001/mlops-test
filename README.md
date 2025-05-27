# GitHub Actions - Workflows Overview
 
This repository contains GitHub Actions workflows to support the training and promotion of machine learning models using Azure Machine Learning (AML).  
 
## Overview
 
There are two primary workflows:
 
1. **Model Training Workflow** – Trains a model in the `dev` environment and registers it to a shared registry.
2. **Model Promotion Workflow** – Promotes a trained model from the shared registry to the `test` environment.
 
---
 
## GitHub Actions Workflows
 
### 1. `deploy-model-training-workflow.yml`
 
**Triggered by:**
- Pushes to the `main` branch
- Manual trigger (`workflow_dispatch`)
 
**Jobs:**
- **Get Config Job**: Retrieves environment-specific variables from GitHub Environment secrets.
- **Register Environment Job**: Calls the reusable workflow `reusable-register-environment.yml` to register the AML environment using:
  - `conda.yml`
  - `train-env.yml`
- **Run ML Pipeline Job**: Calls the reusable workflow `reusable-run-pipeline.yml` to execute the AML training pipeline defined in:
  - `training_pipeline.yaml`
 
---
 
### 2. `deploy-model-promotion-workflow.yaml`
 
**Triggered by:**
- Successful completion of `deploy-model-training-workflow.yml`
- Manual trigger (`workflow_dispatch`)
 
**Jobs:**
- **Get Config Job**: Retrieves environment-specific variables from GitHub Environment secrets.
- **Register Environment Job**: Calls the reusable workflow `reusable-register-environment.yml` to register the AML environment using:
  - `conda.yml`
  - `train-env.yml`
- **Run ML Pipeline Job**: Calls the reusable workflow `reusable-run-pipeline.yml` to execute the AML batch inference pipeline defined in:
  - `batch_inference_pipeline.yaml`
 
---
 
## Key Workflow and Pipeline Files
 
```
.github/workflows/
├── deploy-model-training-workflow.yml        # Workflow for training ML models
├── deploy-model-promotion-workflow.yaml      # Workflow for promoting ML models
├── reusable-register-environment.yml         # Reusable workflow to register AML environments
└── reusable-run-pipeline.yml                 # Reusable workflow to run AML pipelines

featurestore_sample/project/env/
├── conda.yml                                # Conda dependencies for AML environment registration
├── train-env.yml                            # AML environment definition for training
├── online.yml                               # AML environment definition for online inference

featurestore_sample/project/fraud_model/pipelines/
├── batch_inference_pipeline.yaml             # AML Pipeline for batch inference (called by promotion workflow)
└── training_pipeline.yaml                    # AML pipeline for training model (called by training workflow)
```

- The `env` folder contains all environment and dependency files used for registering Azure ML environments.
- In all folders under `featurestore_sample/project/fraud_model/` except for `pipelines`, you will find the relevant Python scripts that are executed as steps in the AML pipelines.
 
---
 
## Set Up & Prerequisites
 
This repository assumes the required Azure infrastructure (AML workspace, compute clusters, storage accounts, networking, and model registry) has been provisioned via Infrastructure-as-Code (IaC) from the `featurestore-iac` repository.
 
### GitHub Environments
 
- Go to **Settings > Environments**
- Create or verify existence of two environments: `dev` and `test`
 
### GitHub Environment Secrets (Required for each environment)
 
| Secret Name             | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `AZURE_CLIENT_ID`       | Client ID of the service principal used for authentication with Azure       |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription ID where resources are deployed                          |
| `AZURE_TENANT_ID`       | Azure Active Directory Tenant ID                                            |
| `AZURE_CLIENT_SECRET`   | Client secret of the service principal                                      |
| `REGISTRY_NAME`         | Name of the Azure Container Registry used                                   |
 
### GitHub Environment Variables (Required for each environment)
 
| Variable Name             | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `AML_WORKSPACE`           | Name of the AML workspace used for experiments and pipelines                |
| `APPLICATION_INSIGHTS`    | Name or ID of the Application Insights resource                             |
| `AZURE_LOCATION`          | Azure region (e.g., `westus`)                                               |
| `CONTAINER_REGISTRY`      | Name of the container registry used                                         |
| `ENABLE_AML_COMPUTECLUSTER` | Flag to enable/provision AML compute cluster (`true` or `false`)          |
| `ENABLE_MONITORING`       | Flag to enable monitoring features (`true` or `false`)                      |
| `KEY_VAULT`               | Name of the Azure Key Vault storing secrets and credentials                 |
| `RESOURCE_GROUP`          | Azure resource group name                                                   |
| `STORAGE_ACCOUNT`         | Name of the Azure Storage Account                                           |
 
> Note:  Make sure values for `dev` and `test` environments align to their respective resource groups and services.
 
---
 
### Environment Deployment Protection 
 
To enforce manual approval for deployments to the `test` environment:
 
1. Navigate to **Settings > Environments > test**
2. Under **Deployment protection rules**, enable **Required reviewers**
3. Add up to 6 reviewers (your own GitHub handle can be added for now)
4. Click **Save protection rules**
 
This ensures promotion workflows to `test` will only run after approval.
 
---
 
### AML Pipeline Configuration
 
Ensure the AML pipelines reference the correct compute and environment values that match the resources created via IaC:
 
- **Default Values**:
  - Compute: `azureml:cpu-cluster-fs`
  - Environment: `azureml:fs-env`
 
You may need to update these in the AML components found in the following files:
 
- `featurestore_sample/project/fraud_model/pipelines/training_pipeline.yaml`
- `featurestore_sample/project/fraud_model/pipelines/batch_inference_pipeline.yaml`
