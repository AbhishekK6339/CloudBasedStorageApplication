from flask import request, flash, redirect, url_for, render_template, send_file, make_response, session
from . import upload_blueprint
from azure.storage.blob import BlobServiceClient
import os
import io

# Define your Azure Storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccforpythonapp;AccountKey=KjwGJhFFS3eSC/nhS5mAqXqNDYPQwv1E9ElaH9Q2rs1gOsfo6XZgaAwtCjX3uZxZchLuQ8bWVVeA+AStphrmKA==;EndpointSuffix=core.windows.net"
# Define the name of the container in Azure Blob Storage
container_name = "storagecontainer"
# Define the directory for local storage (optional)
local_storage_dir = "local_storage/"

@upload_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

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

    # Retrieve list of uploaded files from Azure Blob Storage container
    uploaded_files = []
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        uploaded_files.append(blob.name)

    return render_template('upload.html', uploaded_files=uploaded_files)


@upload_blueprint.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    try:
        # Download the file from Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)

        # Get the content type of the file
        content_type = blob_client.get_blob_properties().content_settings.content_type

        # Read the file content
        file_content = blob_client.download_blob().readall()

        # Create a response with the file content
        response = make_response(file_content)

        # Set the appropriate MIME type and attachment filename for the response
        response.headers['Content-Type'] = content_type
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        flash(f'An error occurred while downloading the file: {e}', 'error')
        return redirect(url_for('upload.upload'))


@upload_blueprint.route('/delete/<string:filename>', methods=['GET'])
def delete(filename):
    try:
        # Delete the file from Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(filename)
        blob_client.delete_blob()

        flash('File deleted successfully!', 'success')
        return redirect(url_for('upload.upload'))

    except Exception as e:
        flash(f'An error occurred while deleting the file: {e}', 'error')
        return redirect(url_for('upload.upload'))
