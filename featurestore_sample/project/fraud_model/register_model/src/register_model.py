from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

import shutil
import argparse
import os


parser = argparse.ArgumentParser("register_model")
parser.add_argument("--model_input", type=str, help="Path to input model data")
parser.add_argument(
    "--model_output", type=str, help="Path of output model to be registered"
)
parser.add_argument(
    "--evaluation_input", type=str, help="Path to input evaluation result data"
)

args = parser.parse_args()

for file_name in os.listdir(args.model_input):
    source = os.path.join(args.model_input, file_name)
    destination = os.path.join(args.model_output, file_name)

    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy(source, destination)

subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = os.environ.get("RESOURCE_GROUP")
workspace = os.environ.get("WORKSPACE_NAME")

#credential = ManagedIdentityCredential(client_id=os.environ.get("AZURE_CLIENT_ID"))

credential = DefaultAzureCredential()

ml_client = MLClient(credential, subscription_id, resource_group, workspace)

ml_client.models.share(name="fraud_model",
                       version="1",
                       registry_name="ml-registry",
                       share_with_name="fraud_model",
                       share_with_version="2.2.0")
