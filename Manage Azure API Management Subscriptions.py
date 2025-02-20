# Automate the creation and management of API Management subscriptions.

from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
api_management_name = "myApiManagement"
subscription_name = "mySubscription"

# Authenticate
credential = DefaultAzureCredential()
api_client = ApiManagementClient(credential, subscription_id)

# Create subscription
subscription = {
    "properties": {
        "displayName": "My Subscription",
        "scope": "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{api_management_name}",
        "state": "active",
    }
}

api_client.subscriptions.create_or_update(
    resource_group_name, api_management_name, subscription_name, subscription
)

# List all subscriptions
subscriptions = api_client.subscriptions.list_by_service(resource_group_name, api_management_name)
for sub in subscriptions:
    print(f"Subscription: {sub.display_name}, State: {sub.state}")

print("API Management subscriptions managed successfully.")
