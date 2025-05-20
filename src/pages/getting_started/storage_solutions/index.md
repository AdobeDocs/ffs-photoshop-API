---
title: Storage Solutions Concept Page
description: This page explains the storage solutions that are acceptable for use with video services.
---
# Storage Solutions

Explore more about the storage solutions you'll need when you're using these APIs.

Some form of user-owned storage (like Amazon S3 buckets) is necessary with these audio and video APIs. Media files (audio or video) and edited transcripts kept in your storage are targeted with pre-signed URLs and used as input for the API.

Learn how to set up your files in these storage solutions to use with the API:

## Using Amazon S3 buckets

  1. Log in to your AWS account.
  2. Go to s3.
  3. Create a new bucket, with any name (for example, *AdobeApiTesting*).
  4. Drag and drop the media file (audio/video) or edited transcript file that you want to provide to the API in the bucket you've created.
  5. Once the upload is complete, select the file and go to **Actions**.
  6. Select the **Share with pre-signed URL** option and enter a duration for the pre-signed URL to be valid.
  7. Copy the generated pre-signed URL to use in the API (it may also copy automatically when you create it).

## Using an Frame.io account

  1. Log in to your Frame.io account.
  2. Create a project (for example, *AdobeApiTesting*).
  3. Open the **Inspect** view of your browser (using Chrome, press f12 and go to the **Network** tab).
  4. Drag and drop the media file (audio/video) or edited transcript file that you want to provide to the API in the bucket.
  5. Select the file, and click **Download**.
  6. In the **Network** tab, you'll see a GET call using a pre-signed URL to use to download the file.
  7. Copy that URL to use in the API.

## Using Frame.io Developer APIs

Refer to [Frame.io API guide](https://developer.frame.io/api/reference/) to create assets and get their pre-signed URL.

## Using Google's direct link service

You can use [Google's direct link service](https://sites.google.com/site/gdocs2direct/?authuser=1&pli=1) to generate downloadable public links for your files by following the instructions on the page.

Before generating the links, be sure your file's visibility in your Google Drive is set to **Anyone with the link**.

# General Workflow

The typical workflow involves making one or more calls to our API, to edit PSD or other image files, and to create new image renditions.

As you begin integrating the Ps APIs into your workflow, there are a few considerations to keep in mind which we've outlined below:

## Input and Output file storage

The Photoshop API works with any public or signed URL. We have documented a few of the most common storage services and how to generate the urls programmatically.

**AWS S3:** Pre-signed GET/PUT URL. For more information about pre-signed urls on S3 you can go [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html). Here are some code samples that show you how to generate your pre-signed urls programmatically:

  - [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/aws-s3/presignedURLs.js) <br />Please note that creating pre-signed urls for AWS S3 requires signature version S3V4, as demonstrated in the sample code.
  - [Python](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.py)

We also have a python [application](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/aws-s3/example.py) that provides a working example of how to call our API using assets stored in AWS S3.

**Google Drive:**: Signed GET/PUT URL. For more information on how to setup your Google drive account for access to creating a signed URL [here](https://www.labnol.org/google-api-service-account-220404). Here are some code samples for getting signed URLs.

  - [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/googledrive/presignedURLs.js)

**Azure:** SAS (Shared Access Signature) for upload/download. For more information on how to generate a Shared Access Signature you can go [here](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.9.0/index.html). Here are some code samples for generating a url with Shared Access Signature.

  - [Node.js](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.js)
  - [Python](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/storage-app/azure/presignedURLs.py)

**Dropbox:** Temporary upload/download URLs.  For more information on how to generate an upload/download you can go [here](https://www.dropbox.com/developers/documentation). You can also create a file upload link for dropbox [here](https://www.dropbox.com/developers/documentation/http/documentation#files-get_temporary_upload_link).  

**Note :** You can test to see if your public url or presigned url is working.

Run the curl command below to see if your input file path is working

```bash
curl -X GET <Your file path> --output <some-file.jpg>
```

  If you're using a pre-signed URL, put your file path within quotes (""):

```bash
curl -X GET "<Your file path>" --output <some-file.jpg>
```

Run the cURL command below to see if your output file path is working:

```bash
curl -X PUT <Your file path> -d <some-file.txt>
```

  If you're using a pre-signed URL, put your file path within quotes (""):

```bash
curl -X PUT "<Your file path>" -d <some-file.txt>
```  

## Current limitations

There are a few limitations to the APIs you should be aware of ahead of time.  

- Multi-part uploads and downloads are not yet supported.
- All the endpoints only support a single file input.
- Error handling is a work in progress. Sometimes you may not see the most helpful of messages.

## Retries

For increased reliability and stability we have added a retry mechanism for all API calls, and have some recommendations on how to handle these:

- The service will retry status codes of 429, 502, 503, 504 three times.
- You should only retry requests that have a 5xx response code. A 5xx error response indicates there was a problem processing the request on the server.
- You should implement an exponential back-off retry strategy with 3 retry attempts.
- You should not retry requests for any other response code.

## Compatibility with Photoshop versions

- The APIs will open any PSD created with Photoshop 1.0 or later.
- When saving as PSD, the APIs will create PSDs compatible with the current shipping Photoshop.
- In regards to "maximize compatibility" referenced in https://helpx.adobe.com/photoshop/using/file-formats.html#maximize_compatibility_for_psd_and_psb_files  the API's default to "yes"
