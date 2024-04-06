from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from azure.storage.blob import BlobServiceClient

upload_blueprint = Blueprint('upload', __name__)

# Define your Azure Storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccforpythonapp;AccountKey=KjwGJhFFS3eSC/nhS5mAqXqNDYPQwv1E9ElaH9Q2rs1gOsfo6XZgaAwtCjX3uZxZchLuQ8bWVVeA+AStphrmKA==;EndpointSuffix=core.windows.net"
# Define the name of the container in Azure Blob Storage
container_name = "storageContainer"
# Define the directory for local storage
local_storage_dir = "local_storage/"


@upload_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # Save the file to local storage
        local_file_path = os.path.join(local_storage_dir, file.filename)
        file.save(local_file_path)

        # Upload the file to Azure Blob Storage
        blob_name = file.filename
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data)

        flash('File uploaded successfully', 'success')
        return redirect(url_for('/upload'))  # Redirect to the same upload page after handling upload

    return render_template('upload.html')
