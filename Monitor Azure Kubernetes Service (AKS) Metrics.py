# Monitor CPU and memory usage for an AKS cluster using Azure Monitor.

from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

# Define variables
subscription_id = "your-subscription-id"
resource_id = "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ContainerService/managedClusters/myAKSCluster"

# Authenticate
credential = DefaultAzureCredential()
monitor_client = MonitorManagementClient(credential, subscription_id)

# Query metrics
metrics_data = monitor_client.metrics.list(
    resource_id,
    metricnames="cpuUsage,memoryUsage",
    interval="PT1M",
    timespan="PT1H",
)

for metric in metrics_data.value:
    print(f"Metric: {metric.name.value}")
    for time_series in metric.timeseries:
        for data in time_series.data:
            print(f"Timestamp: {data.time_stamp}, Value: {data.average}")
