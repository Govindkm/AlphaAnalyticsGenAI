from google.cloud import pubsub_v1
import time
import json

# Replace with your project ID and topic name
project_id = "a208960-alphaanalytics-sandbox"
topic_name = "alpha_analytics_messages"

# Your message data
data = {"file_uploaded": "testagain.txt"}

# Create a Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()

# Construct the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Encode the data as bytes
data_bytes = json.dumps(data).encode("utf-8")

# Publish the message
future = publisher.publish(topic_path, data=data_bytes)

# Wait for publishing to complete
print(f"Published message ID: {future.result()}")

