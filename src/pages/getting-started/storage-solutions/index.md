---
title: Storage Solutions
description: Learn how to set up and use storage solutions with the Photoshop API.,
hideBreadcrumbNav: true
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
  - https://github.com/AEAbreu-hub
keywords:
  - storage
  - S3
  - pre-signed URL
  - Frame.io
  - Google Drive
  - Azure
  - Dropbox
---

# Storage Solutions

Learn about the storage solutions you'll need when using the Photoshop API.

## Set up your storage

You'll need some form of user-owned storage (like Amazon S3 buckets) to use with the Photoshop API. Your media files and edited transcripts are stored in your storage and accessed via pre-signed URLs for API input.

### Using Amazon S3 buckets

1. Log in to your AWS account.
2. Go to S3.
3. Create a new bucket (for example, *AdobeApiTesting*).
4. Upload your media file to the bucket.
5. Once the upload is complete, select the file and go to **Actions**.
6. Select **Share with pre-signed URL** and set the URL duration.
7. Copy the generated pre-signed URL for use with the API.

### Using a Frame.io account

1. Log in to your Frame.io account.
2. Create a project (for example, *AdobeApiTesting*).
3. Open your browser's **Inspect** view (in Chrome, press F12 and go to the **Network** tab).
4. Upload your media file.
5. Select the file and click **Download**.
6. In the **Network** tab, you'll see a GET request using a pre-signed URL.
7. Copy that URL for use with the API.

### Using Frame.io Developer API

Refer to the [Frame.io API guide](https://developer.frame.io/api/reference/) to create assets and get pre-signed URLs.

### Using Google's direct link service

You can use [Google's direct link service](https://sites.google.com/site/gdocs2direct/?authuser=1&pli=1) to generate downloadable public links for your files. Before generating the links, set your file's visibility in Google Drive to **Anyone with the link**.

## Ready-to-use workflows

A typical workflow makes calls to the Photoshop API to edit *.psd* or other image files and generate new image variations. The Photoshop API works with any public or signed URL.

We've documented the most common storage services and how to generate URLs programmatically.

### AWS S3

A pre-signed GET/PUT URL. See the docs for [more information about pre-signed URLs on S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html).

Workflow samples:

- [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/aws-s3/presignedURLs.js) - Note that creating pre-signed URLs for AWS S3 requires signature version S3V4.
- [Python](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.py)
- [Python application](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/aws-s3/example.py) that demonstrates how to call the API using assets stored in AWS S3.

### Google Drive

A signed GET/PUT URL. See the docs for [setting up your Google Drive account for signed URLs](https://www.labnol.org/google-api-service-account-220404).

Workflow samples:

- [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/googledrive/presignedURLs.js)

### Azure

A SAS (Shared Access Signature) for upload/download. See the docs for [generating a Shared Access Signature](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.9.0/index.html).

Workflow samples:

- [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.js)
- [Python](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.py)

### Dropbox

Temporary upload/download URLs. See the docs for [generating upload/download URLs](https://www.dropbox.com/developers/documentation). You can also [create a file upload link for Dropbox](https://www.dropbox.com/developers/documentation/http/documentation#files-get_temporary_upload_link).

### Test your URLs

Test if your public URL or pre-signed URL is working with the following commands.

Test your input file path:

```bash
curl -X GET "<your_file_path>" \
--output <some-file.jpg>
```

Test your output file path:

```bash
curl -X PUT "<your_file_path>" \
-d <some-file.txt>
```
