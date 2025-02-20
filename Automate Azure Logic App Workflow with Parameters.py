# Deploy a Logic App workflow with dynamic parameters and triggers.

from azure.identity import DefaultAzureCredential
from azure.mgmt.logic import LogicManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
logic_app_name = "myLogicApp"

# Authenticate
credential = DefaultAzureCredential()
logic_client = LogicManagementClient(credential, subscription_id)

# Define Logic App workflow
workflow = {
    "properties": {
        "definition": {
            "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "param1": {"type": "string", "defaultValue": "value1"}
            },
            "triggers": {
                "Recurrence": {
                    "type": "Recurrence",
                    "recurrence": {"frequency": "Day", "interval": 1},
                }
            },
            "actions": {
                "Send_email": {
                    "type": "Http",
                    "inputs": {
                        "method": "POST",
                        "uri": "https://example.com/send-email",
                        "body": "@parameters('param1')",
                    },
                }
            },
        },
        "parameters": {"param1": {"value": "Hello World"}},
    }
}

logic_client.workflows.create_or_update(resource_group_name, logic_app_name, workflow)
print("Logic App deployed successfully.")
