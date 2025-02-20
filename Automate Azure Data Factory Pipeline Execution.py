from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.datafactory.models import *

# Define variables
subscription_id = "your-subscription-id"
resource_group_name = "myResourceGroup"
data_factory_name = "myDataFactory"
pipeline_name = "myPipeline"

# Authenticate
credential = DefaultAzureCredential()
adf_client = DataFactoryManagementClient(credential, subscription_id)

# Define pipeline activities
activity = CopyActivity(
    name="CopyBlobToBlob",
    source=BlobSource(),
    sink=BlobSink(),
    type_properties={"source": {}, "sink": {}},
)

pipeline = PipelineResource(activities=[activity])

# Create pipeline
adf_client.pipelines.create_or_update(resource_group_name, data_factory_name, pipeline_name, pipeline)

# Execute pipeline
run_response = adf_client.pipelines.create_run(
    resource_group_name, data_factory_name, pipeline_name
)

# Monitor pipeline execution
while True:
    run = adf_client.pipeline_runs.get(
        resource_group_name, data_factory_name, run_response.run_id
    )
    if run.status in ["Succeeded", "Failed", "Cancelled"]:
        print(f"Pipeline run finished with status: {run.status}")
        break
    time.sleep(10)

print("Pipeline executed successfully.")
