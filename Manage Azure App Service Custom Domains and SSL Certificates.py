from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.network import NetworkManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
app_service_name = "myWebApp"
custom_domain = "www.example.com"
certificate_name = "example-cert"

# Authenticate
credential = DefaultAzureCredential()
web_client = WebSiteManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Add custom domain to App Service
web_client.app_service_domains.create_or_update(
    resource_group_name,
    custom_domain,
    {"contact_admin_email": "admin@example.com", "privacy": "Public"},
).result()

# Bind custom domain to App Service
web_client.web_apps.create_or_update_hostname_binding(
    resource_group_name,
    app_service_name,
    custom_domain,
    {"site_name": app_service_name},
).result()

# Upload SSL certificate
with open("path/to/certificate.pfx", "rb") as cert_file:
    cert_content = cert_file.read()

certificate = web_client.certificates.create_or_update(
    resource_group_name,
    certificate_name,
    {
        "password": "your-certificate-password",
        "pfx_blob": cert_content,
    },
).result()

# Bind SSL certificate to custom domain
web_client.web_apps.create_or_update_ssl_binding(
    resource_group_name,
    app_service_name,
    custom_domain,
    {
        "ssl_state": "SniEnabled",
        "thumbprint": certificate.thumbprint,
        "virtual_ip": None,
    },
).result()

print("Custom domain and SSL certificate configured successfully.")
