# Deploy an Azure Cosmos DB account with autoscale enabled.

from azure.identity import DefaultAzureCredential
from azure.mgmt.cosmosdb import CosmosDBManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
cosmos_db_name = "myCosmosDB"

# Authenticate
credential = DefaultAzureCredential()
cosmos_client = CosmosDBManagementClient(credential, subscription_id)

# Create Cosmos DB account
cosmos_client.database_accounts.begin_create_or_update(
    resource_group_name,
    cosmos_db_name,
    {
        "location": "eastus",
        "kind": "GlobalDocumentDB",
        "properties": {
            "databaseAccountOfferType": "Standard",
            "enable_automatic_failover": True,
            "capabilities": [{"name": "EnableAutoscale"}],
        },
    },
).result()

# Configure autoscale for database
cosmos_client.sql_resources.begin_create_update_sql_database(
    resource_group_name,
    cosmos_db_name,
    "myDatabase",
    {
        "resource": {
            "id": "myDatabase",
            "throughput": None,  # Use autoscale
            "autoscale_settings": {"max_throughput": 4000},
        }
    },
).result()

print("Cosmos DB deployed with autoscale.")
