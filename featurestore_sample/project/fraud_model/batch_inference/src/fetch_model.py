from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
#from azure.identity import ManagedIdentityCredential
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

import argparse
import shutil
import os

BASE_PATH = "./fraud_model/model_output"

parser = argparse.ArgumentParser("fetch")
parser.add_argument("--model_output", type=str, help="Path of output model")
args = parser.parse_args()

#credential = ManagedIdentityCredential(client_id="...") #Needs to change to DefaultAzureCredential if not using UAMI
credential = DefaultAzureCredential()

ml_client = MLClient(credential=credential,
                     subscription_id="...",
                     resource_group_name="...",
                     workspace_name="...",
                     )

ml_client_registry = MLClient(credential=credential,
                        registry_name="...",
                        registry_location="...")

ml_client_registry.models.download(name="fraud_model", version="1")

file_model = Model(
    path=BASE_PATH,
    type=AssetTypes.CUSTOM_MODEL,
    name="fraud_model"
)

ml_client.models.create_or_update(file_model)

shutil.copy(
    os.path.join(BASE_PATH, "feature_retrieval_spec.yaml"), args.model_output
)

shutil.copy(
    os.path.join(BASE_PATH, "clf.pkl"), args.model_output
)