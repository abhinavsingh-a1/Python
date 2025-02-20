#Deploy an Event Hub namespace with capture enabled to store data in Azure Blob Storage.

from azure.identity import DefaultAzureCredential
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.storage import StorageManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
namespace_name = "myEventHubNamespace"
storage_account_name = "mystorageaccount"

# Authenticate
credential = DefaultAzureCredential()
eventhub_client = EventHubManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# Create storage account
storage_client.storage_accounts.begin_create(
    resource_group_name,
    storage_account_name,
    {
        "sku": {"name": "Standard_LRS"},
        "kind": "StorageV2",
        "location": "eastus",
    },
).result()

# Create Event Hub namespace
eventhub_client.namespaces.begin_create_or_update(
    resource_group_name,
    namespace_name,
    {
        "location": "eastus",
        "sku": {"name": "Standard"},
        "capture_description": {
            "enabled": True,
            "destination": {
                "name": "EventHubCapture",
                "storage_account_resource_id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}",
                "blob_container": "eventhub-capture",
            },
        },
    },
).result()

print("Event Hub namespace deployed with capture enabled.")
