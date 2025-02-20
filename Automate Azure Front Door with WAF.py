from azure.identity import DefaultAzureCredential
from azure.mgmt.cdn import CdnManagementClient
from azure.mgmt.network import NetworkManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
front_door_name = "myFrontDoor"
waf_policy_name = "myWAFPolicy"

# Authenticate
credential = DefaultAzureCredential()
cdn_client = CdnManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Create WAF policy
waf_policy = {
    "sku": {"name": "Classic_AzureFrontDoor"},
    "custom_rules": [
        {
            "name": "BlockSQLInjection",
            "priority": 1,
            "rule_type": "MatchRule",
            "matchConditions": [
                {
                    "match_variable": "RequestUri",
                    "operator": "Contains",
                    "negate_condition": False,
                    "match_values": ["sql"],
                }
            ],
            "action": "Block",
        }
    ],
}

cdn_client.waf_policies.create_or_update(
    resource_group_name, waf_policy_name, waf_policy
)

# Associate WAF policy with Front Door
front_door_config = {
    "properties": {
        "frontendEndpoints": [
            {"name": "default", "hostName": "www.example.com", "wafPolicyLink": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/frontdoorWebApplicationFirewallPolicies/{waf_policy_name}"}
        ]
    }
}

cdn_client.front_doors.begin_create_or_update(
    resource_group_name, front_door_name, front_door_config
).result()

print("Front Door configured with WAF successfully.")
