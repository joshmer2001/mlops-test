# Azure MLOpsv3 Accelerator

This accelerator provides infrastructure as code, CI/CD pipelines, and templates for implementing MLOps best practices with Azure Machine Learning.

## Architecture

The accelerator uses a multi-environment approach with separate development, test, and production environments, each with their own resource group. A shared model registry enables model promotion across environments.

![image](https://github.com/user-attachments/assets/d4b5f1f1-52ec-48b1-8fa5-c0bd4453a055)

### Environment Separation

- Each environment (dev, test, prod) has its own:
  - Resource group with naming pattern: `mlops-{env}-rg`
  - Environment-specific storage accounts and ML workspaces
  - Connection to the shared model registry

- Shared resources:
  - Shared model registry in `mlops-shared-rg` resource group that enables:
    - Central model storage and versioning
    - Central feature store 
    - Model promotion workflow across environments
    - Consistent model management

## ML Pipeline Components

```
/featurestore_sample/
├── automation-test/             # Automation testing
├── featurestore/                # Feature engineering
├── notebooks/                   # Jupyter notebook code
├──project/
   ├── env/                      # Python environment definition
   ├── fraud_model/
      ├── batch_inference        # Batch inference Python code
      ├── evaluate               # Evaluate model Python code
      ├── pipelines              # ML pipeline definitions
      ├── register               # Regiter model Python code
      ├── train                  # Train model Python code
```

<<<<<<< HEAD
- The `env` folder contains all environment and dependency files used for registering Azure ML environments.
- In all folders under `featurestore_sample/project/fraud_model/` except for `pipelines`, you will find the relevant Python scripts that are executed as steps in the AML pipelines.
 
---
 
## Set Up & Prerequisites
 
This repository assumes the required Azure infrastructure (AML workspace, compute clusters, storage accounts, networking, and model registry) has been provisioned via Infrastructure-as-Code (IaC) from the `featurestore-iac` repository. If not, follow the instructions [Base Infrastructure - Deploy Azure MLOps Terraform Infrastructure](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/README.md) to set up the infrastructure first
 
### GitHub Environments
 
- Go to **Settings > Environments**
- Create or verify existence of two environments: `dev` and `test`
=======
## Getting Started
 - Following approach / steps to be consisdered. Specific prerequisites are covered in each steps and details are given in below links
     1. Phase 1: [Base Infrastructure - Deploy Azure MLOps Terraform Infrastructure](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/README.md)
     2. Phase 2: [Run Notebooks - manual implementation of the flow](./featurestore_sample/notebooks/sdk_only/)
     3. Phase 3: [Run Github Action - CI/CD Implementation](https://github.com/mlops-org-sains/featurestore-mlops/blob/main/README.md)
>>>>>>> 5f413c9b73c4b38c1569fae9e8040806891ae5e1

### Prerequisites

This section outlines the general prerequisites for running the accelerator. For detailed **mandatory requirements and guidance**, please refer to the notes provided under each phase above.

| Category | Requirement |
|----------|-------------|
| **Azure Resources** | Azure subscription, Azure Machine Learning workspace, Azure Key Vault, Azure Container Registry, Azure Storage Account |
| **Infrastructure Setup** | Terraform (if infra-as-code is used) |
| **Development Tools** | Python 3.8+, Azure CLI, Azure SDK, Azure ML CLI v2, Git |
| **CI/CD Tools** | Azure DevOps or GitHub Actions configured with service connections to Azure |
| **Permissions** | Contributor or Owner role on the Azure subscription/resource group, along with the necessary privileges to create Azure resources |
| **Python Dependencies** | `azureml-sdk`, `mlflow`, `pandas`, `scikit-learn`, `joblib`, and other machine learning libraries specified in each phase above and listed in the conda.yml file |
| **Compute Targets** | Azure ML compute clusters or attached compute instances for training and inference and serverless spark instance |
| **Storage** | Datastores registered in Azure ML for datasets and model artifacts |



### For detailed documentation:
- [Phase1-Infrastructure.md](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/docs/Infrastructure.md) - Infrastructure architecture overview
- [Terraform-Setup.md](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/docs/Terraform-Setup.md) - Detailed setup and deployment guide
- [Model-Registry.md](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/docs/Model-Registry.md) - Model registry configuration and usage
- [Required Tags](https://github.com/mlops-org-sains/featurestore-iac/blob/workshop-config-changes/docs/Required-Tags.md) - Required Tags Implementation

