from flask import request, flash, redirect, url_for, render_template
from . import upload_blueprint
from azure.storage.blob import BlobServiceClient, BlobClient
import os

# Define your Azure Storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccforpythonapp;AccountKey=KjwGJhFFS3eSC/nhS5mAqXqNDYPQwv1E9ElaH9Q2rs1gOsfo6XZgaAwtCjX3uZxZchLuQ8bWVVeA+AStphrmKA==;EndpointSuffix=core.windows.net"
# Define the name of the container in Azure Blob Storage
container_name = "storagecontainer"
# Define the directory for local storage (optional)
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

        try:
            # Save the file to local storage (optional)
            local_file_path = os.path.join(local_storage_dir, file.filename)
            file.save(local_file_path)

            # Upload the file to Azure Blob Storage
            blob_name = file.filename
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)

            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data)

            flash('File uploaded successfully!', 'success')

            # Delete the local file after successful upload (optional)
            os.remove(local_file_path)

            return redirect(url_for('upload.upload'))

        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            return redirect(request.url)

    return render_template('upload.html')
