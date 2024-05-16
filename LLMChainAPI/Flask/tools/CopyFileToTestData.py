import json
from os import path, makedirs
import uuid
from google.cloud import storage

BUCKET_NAME = "alpha-analytics-bucket"

current_dir = path.dirname(__file__)
json_folder = path.join(current_dir, "jsonFiles")

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
            

def upload_to_gcs(source_file_name):
    """
    Uploads a file to the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    filename = path.basename(source_file_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(source_file_name)


def saveJson(response_data):
    # Create the 'jsonFiles' folder if it doesn't exist
    if not path.exists(json_folder):
        makedirs(json_folder)

    try:
        # Generate a UUID to use as the filename
        filenameconstant = "alphaanalytics.json"
        filename = path.join(json_folder, filenameconstant)
        result = [json.dumps(record) for record in response_data]
        with open(filename, 'w') as obj:
            for i in result:
              obj.write(i+'\n')
        
        # Save the JSON data into a disk file
        # with open(filename, "w") as file:
        #    json.dump(data, file)
        upload_to_gcs(filename)
        
    except Exception as e:
        print(f"Error creating file path, Error: {e}")