# Automate the creation of access policies for an Azure Key Vault.

from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
key_vault_name = "myKeyVault"

# Authenticate
credential = DefaultAzureCredential()
keyvault_client = KeyVaultManagementClient(credential, subscription_id)

# Create Key Vault
keyvault_client.vaults.begin_create_or_update(
    resource_group_name,
    key_vault_name,
    {
        "location": "eastus",
        "properties": {
            "sku": {"family": "A", "name": "standard"},
            "tenant_id": "your-tenant-id",
            "access_policies": [
                {
                    "tenant_id": "your-tenant-id",
                    "object_id": "user-object-id",
                    "permissions": {
                        "keys": ["get", "list", "create"],
                        "secrets": ["get", "set", "delete"],
                    },
                }
            ],
        },
    },
).result()

print("Key Vault access policies configured successfully.")
