---
title: Triggering an Event from the Photoshop API
description: This guide explains how to trigger webhook events from the Photoshop API by including your IMS ORG ID in API calls.
hideBreadcrumbNav: true
keywords:
  - webhook events
  - IMS ORG ID
  - event handling
  - job status
  - API events
contributors:
  - https://github.com/AEAbreu-hub
---

# Triggering an Event

Trigger webhook events from the Photoshop API by including your IMS ORG ID in API calls.

## Receive events

To understand what webhook events are and how to set up your application to use them, start with [the page on using webhooks and events](../../getting-started/webhooks/index.md).

To receive Photoshop events in your webhook application, pass the IMS ORG ID in a header when you make an API call to initiate a job:

```shell
-H 'x-gw-ims-org-id: <YOUR_IMS_ORG_ID>'
```

## Retrieving a PSD manifest

The `/v2/generate-manifest` API takes an input PSD and generates a JSON manifest from it. The JSON manifest provides a representation of all the layer objects contained in the PSD document.

Using `Example.psd`, with the use case of a document stored in your external storage, a typical cURL call might look like this:

```shell
curl -X POST \
  https://photoshop-api.adobe.io/v2/generate-manifest \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -H 'x-gw-ims-org-id: <YOUR_IMS_ORG_ID>' \
  -d '{
  "image": {
    "source": {
      "url": "<SIGNED_GET_URL>"
    }
  },
  "outputs": [
    {
      "destination": {
        "url": "<MANIFEST_OUTPUT_URL>"
      },
      "mediaType": "application/json"
    }
  ]
}'
```

This initiates an asynchronous job and returns a response containing the `jobId` and a `statusUrl` to [poll for job status and the JSON manifest](/guides/get-job-status/index.md).

**Example response:**

```json
{
  "jobId": "63c6e812-6cb8-43de-8a60-3681a9ec6feb",
  "statusUrl": "https://photoshop-api.adobe.io/v2/status/63c6e812-6cb8-43de-8a60-3681a9ec6feb"
}
```

## Receive the job's status on the webhook application

When the job finishes, your webhook application receives a CloudEvents-formatted event. The `data` field contains the job's status. To get the job's outputs, [poll for the job status](/guides/get-job-status/index.md) using the `jobId`.

**Example event:**

```json
{
  "specversion": "1.0",
  "type": "com.adobe.photoshop-api.v2.generate-manifest.success",
  "source": "urn:aio_provider_metadata:cc_ffs_ps_job_status",
  "id": "7e3a89ce-d1f5-4b55-a9fc-682e3ac535e2",
  "time": "2025-01-20T10:40:00Z",
  "datacontenttype": "application/json",
  "requestorclientid": "cis_services",
  "adobeinternal": {
    "imsOrg": "<YOUR_IMS_ORG_ID>"
  },
  "data": {
    "jobId": "63c6e812-6cb8-43de-8a60-3681a9ec6feb",
    "status": "succeeded",
    "createdTime": "2025-01-20T10:35:00Z",
    "modifiedTime": "2025-01-20T10:40:00Z"
  }
}
```

For the full event structure and the list of event types, see [the page on using webhooks and events](../../getting-started/webhooks/index.md).
