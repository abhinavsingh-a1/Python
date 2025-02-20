from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
import time

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
server_name = "mySqlServer"
database_name = "myDatabase"
vault_name = "myRecoveryServicesVault"

# Authenticate
credential = DefaultAzureCredential()
sql_client = SqlManagementClient(credential, subscription_id)
backup_client = RecoveryServicesBackupClient(credential, subscription_id)

# Enable backup for SQL database
protected_item = {
    "properties": {
        "protectedItemType": "AzureSqlDatabaseProtectedItem",
        "policyId": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.RecoveryServices/vaults/{vaultName}/backupPolicies/DefaultPolicy",
    }
}
backup_client.protected_items.create_or_update(
    vault_name=vault_name,
    resource_group_name=resource_group_name,
    fabric_name="Azure",
    container_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name}",
    protected_item_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name};{database_name}",
    parameters=protected_item,
).result()

# Trigger backup
backup_job = backup_client.backup_protectable_items.trigger_backup(
    vault_name=vault_name,
    resource_group_name=resource_group_name,
    fabric_name="Azure",
    container_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name}",
    protected_item_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name};{database_name}",
).result()

# Wait for backup to complete
time.sleep(300)  # Adjust based on backup duration

# Restore database
restore_request = {
    "properties": {
        "objectType": "AzureSqlRestoreRequest",
        "recoveryPointId": backup_job.properties.recovery_point_id,
        "targetDatabaseName": "restoredDatabase",
        "targetServerName": server_name,
    }
}
restore_job = backup_client.restores.trigger(
    vault_name=vault_name,
    resource_group_name=resource_group_name,
    fabric_name="Azure",
    container_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name}",
    protected_item_name=f"SQLDataBase;iaasvmcontainer;{resource_group_name};{server_name};{database_name}",
    parameters=restore_request,
).result()

print("Backup and restore completed successfully.")
