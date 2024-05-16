import functions_framework
from google.cloud import bigquery
from google.cloud import pubsub_v1

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    #taking the metadata of the file
    data = cloud_event.data

    print('data fetched')

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    #project id
    project_id="a208960-alphaanalytics-sandbox"
    dataset_id="API_Oil_Production"
    table_name_id=name
    table_name=table_name_id.split('.')[0]

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = f"""{project_id}.{dataset_id}.{table_name}"""

    # TODO(developer): Set the source_uris to point to your data in Google Cloud
    #variable declaring bucket name
    bucket_name="alpha-analytics-bucket"

    source_uri=f"""gs://{bucket_name}/{name}"""

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
    )

    #Connecting Source URI with URI
    uri = source_uri

    load_job = client.load_table_from_uri(
        uri,
        table_id,
        #location="US",  # Must match the destination dataset location.
        job_config=job_config,
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

    message_data = f"{"file_uploaded": table_name}".encode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, "alpha_analytics_messages")
    future = publisher.publish(topic_path, data=message_data)
    print(f"Message published: {future.result()}")
