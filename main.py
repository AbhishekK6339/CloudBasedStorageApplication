from flask import Flask, request
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Define your Azure Storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccforpythonapp;AccountKey=KjwGJhFFS3eSC/nhS5mAqXqNDYPQwv1E9ElaH9Q2rs1gOsfo6XZgaAwtCjX3uZxZchLuQ8bWVVeA+AStphrmKA==;EndpointSuffix=core.windows.net"
# Define the name of the container in Azure Blob Storage
container_name = "storageContainer"
# Define the directory for local storage
local_storage_dir = "local_storage/"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]
    if file.filename == "":
        return "No selected file"

    # Save the file to local storage
    local_file_path = os.path.join(local_storage_dir, file.filename)
    file.save(local_file_path)

    # Upload the file to Azure Blob Storage
    blob_name = file.filename
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)

    return "File uploaded successfully"

if __name__ == "__main__":
    app.run(debug=True)
