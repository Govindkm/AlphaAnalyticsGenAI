from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound

def upload_to_bigquery(event, context):
    # Extracting bucket and file information from the event
    bucket_name = "alpha-analytics-bucket"
    file_name = event['name']
    
    # Configuring BigQuery client
    bq_client = bigquery.Client()
    
    # Configuring Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Define BigQuery dataset and table information
    project_id="a208960-alphaanalytics-sandbox"
    dataset_id = 'API_Oil_Production'
    table_id = f"""{project_id}.{dataset_id}.{file_name}"""
    
    # Check if the dataset exists, create it if it doesn't
    dataset_ref = bq_client.dataset(dataset_id)
    try:
        bq_client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = bq_client.create_dataset(dataset)
    
    # Define the job configuration
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True
    )
    
    # Load data from Cloud Storage to BigQuery
    uri = f'gs://{bucket_name}/{file_name}'
    load_job = bq_client.load_table_from_uri(
        uri, dataset_ref.table(table_id), job_config=job_config
    )
    
    # Wait for the job to complete
    load_job.result()
    
    print(f'File {file_name} uploaded to BigQuery table {dataset_id}.{table_id}')

# The following lines are for testing the function locally
# Replace 'your-bucket-name' and 'your-file-name.csv' with actual values
# upload_to_bigquery({'bucket': 'your-bucket-name', 'name': 'your-file-name.csv'}, None)
