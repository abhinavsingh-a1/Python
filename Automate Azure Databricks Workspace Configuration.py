from azure.identity import DefaultAzureCredential
from azure.mgmt.databricks import DatabricksClient
from azure.mgmt.network import NetworkManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
workspace_name = "myDatabricksWorkspace"
vnet_name = "databricks-vnet"
subnet_name = "databricks-subnet"
location = "eastus"

# Authenticate
credential = DefaultAzureCredential()
databricks_client = DatabricksClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Create virtual network and subnet
vnet = network_client.virtual_networks.begin_create_or_update(
    resource_group_name,
    vnet_name,
    {"location": location, "address_space": {"address_prefixes": ["10.0.0.0/16"]}},
).result()

subnet = network_client.subnets.begin_create_or_update(
    resource_group_name,
    vnet_name,
    subnet_name,
    {"address_prefix": "10.0.0.0/24"},
).result()

# Create Databricks workspace
workspace = databricks_client.workspaces.begin_create_or_update(
    resource_group_name,
    workspace_name,
    {
        "location": location,
        "properties": {
            "managed_resource_group_id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}",
            "parameters": {
                "customPrivateSubnetName": {"value": subnet.name},
                "customPublicSubnetName": {"value": "public-subnet"},
            },
        },
    },
).result()

# Configure managed identity for Databricks
identity = workspace.identity
databricks_client.workspaces.update(
    resource_group_name,
    workspace_name,
    {"identity": identity},
)

print("Databricks workspace configured successfully.")
