# Deploy an Azure Container Registry with geo-replication to multiple regions.

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
registry_name = "myContainerRegistry"

# Authenticate
credential = DefaultAzureCredential()
acr_client = ContainerRegistryManagementClient(credential, subscription_id)

# Create container registry
acr_client.registries.begin_create(
    resource_group_name,
    registry_name,
    {
        "sku": {"name": "Premium"},
        "location": "eastus",
        "admin_user_enabled": True,
    },
).result()

# Add geo-replication to West US
acr_client.replications.begin_create(
    resource_group_name,
    registry_name,
    "westus",
    {"location": "westus"},
).result()

print("Container registry deployed with geo-replication.")
