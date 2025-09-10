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

To understand what webhook events are and how to set up your application to use them, start with [the page on using webhooks and events](../../getting_started/webhooks/).

To receive Photoshop events in your webhook application, pass the IMS ORG ID in a header when you make an API call to initiate a job:

```shell
-H 'x-gw-ims-org-id: <YOUR_IMS_ORG_ID>'
```

## Retrieving a PSD manifest

The `/documentManifest` API can take one or more input PSDs and generate JSON manifest files from them. The JSON manifest provides a representation of all the layer objects contained in the PSD document.

Using `Example.psd`, with the use case of a document stored in your external storage, a typical cURL call might look like this:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentManifest \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -H 'x-gw-ims-org-id: <YOUR_IMS_ORG_ID>' \
  -d '{
  "inputs": [
    {
      "href":"<SIGNED_GET_URL>",
      "storage":"<storage>"
    }
  ]
}'
```

This initiates an asynchronous job and returns a response containing the href to [poll for job status and the JSON manifest](/guides/get_job_status/).

**Example response:**

```json
{
    "_links": {
        "self": {
            "href": "https://image.adobe.io/pie/psdService/status/63c6e812-6cb8-43de-8a60-3681a9ec6feb"
        }
    }
}
```

## Receive the job's status on the webhook application

The value in the `body` field contains the result of the job.

**Example response:**

```json
{
  "event_id": "b412a90e-8bc0-4f0d-931e-9e9b8d24993d",
  "event": {
    "header": {
      "msgType": "JOB_COMPLETION_STATUS",
      "msgId": "8afa1a46-2733-406c-a646-e1c1acdee333",
      "imsOrgId": "<YOUR_IMS_ORG_ID>",
      "eventCode": "photoshop-job-status",
      "_pipelineMeta": {
        "pipelineMessageId": "1586288145511:631472:VA7_A1:142:0"
      },
      "_smarts": {
        "definitionId": "3ee6c9056a9d72fc40e09ddf5fdbb0af752e8e49",
        "runningSmartId": "psmart-yw6wosjksniuuathenny"
      },
      "_adobeio": {
        "imsOrgId": "<YOUR_IMS_ORG_ID>",
        "providerMetadata": "di_event_code",
        "eventCode": "photoshop-job-status"
      }
    },
    "body": {
      "jobId": "63c6e812-6cb8-43de-8a60-3681a9ec6feb",
      "outputs": [
        {
          "status": "succeeded",
          "layers": [
            {
              "id": 2,
              "index": 0,
              "type": "layer",
              "name": "Layer",
              "locked": false,
              "visible": true,
              "bounds": {
                "top": 0,
                "left": 0,
                "width": 100,
                "height": 100
              },
              "blendOptions": {
                "opacity": 100,
                "mode": "normal"
              }
            }
          ],
          "document": {
            "name": "test.psd",
            "width": 1000,
            "height": 1000,
            "bitDepth": 8,
            "imageMode": "rgb",
            "photoshopBuild": "Adobe Creative Imaging Service"
          }
        }
      ],
      "_links":{
        "self":{
          "href":"https://image.adobe.io/pie/psdService/status/8ec6e4f5-b580-41ac-b693-a72f150fec59"
        }
      }
    }
  }
}
```
