import json
import os
from google.cloud import storage

# Replace these with your actual values
BUCKET_NAME = "alpha-analytics-bucket"
SOURCE_FOLDER = os.path.join(os.path.dirname(__file__), "QueriedFiles";

def verify_json(file_path):
    """
    Verifies if a file is valid JSON.
    Returns True if valid, False otherwise.
    """
    try:
        with open(file_path, "r") as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False

def convert_to_json_ndjson(file_path):
    """
    Converts a JSON file to JSON Newline Delimited format.
    Yields each line of the NDJSON data.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
        for item in data:
            yield json.dumps(item) + "\n"

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def main():
    """
    Iterates through files, verifies, converts, and uploads to GCS.
    """
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(SOURCE_FOLDER, filename)
            if verify_json(file_path):
                ndjson_data = convert_to_json_ndjson(file_path)
                destination_blob_name = f"{filename}.ndjson"
                upload_to_gcs(BUCKET_NAME, ndjson_data, destination_blob_name)
                print(f"Uploaded {filename} to {BUCKET_NAME} as {destination_blob_name}")
            else:
                print(f"Skipping invalid JSON file: {filename}")

if __name__ == "__main__":
    main()