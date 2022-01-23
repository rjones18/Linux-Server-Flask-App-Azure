import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request, redirect

app = Flask(__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING','DefaultEndpointsProtocol=https;AccountName=regj;AccountKey=P>container_name = "photos" # container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to >try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to int>    container_client.get_container_properties() # get properties of the container to force exception to be thrown if co>except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account>
@app.route("/")
def view_photos():
    blob_items = container_client.list_blobs() # list all the blobs in the container

    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name) # get blob client to interact with the blob and >        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/>".format(blob_client.url) # get >
    img_html += "</div>"

    # return the html with the images
    return """
    <head>
    <!-- CSS only -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity>    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">Food App</a>
            </div>
        </nav>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
                <h3>Upload new File</h3>
                <div class="form-group">
		<form method="post" action="/upload-photos"
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-cont>                            <input type="submit" class="btn btn-primary">
                        </div>
                    </form>
                </div>
            </div>

    """ + img_html + "</div></body>"

#flask endpoint to upload a photo
@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""

    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file) # upload the file to the container using the filename as >            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames

    return redirect('/')
