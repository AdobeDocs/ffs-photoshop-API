---
title: Create a mask
description: Learn how to generate semantic object and background masks using the Generate Object Masks API endpoint for image compositing and editing
hideBreadcrumbNav: true
keywords:
  - create mask
  - image mask
  - object mask
  - mask generation
  - image compositing
contributors:
  - https://github.com/AEAbreu-hub
---

# Create Mask

Generate semantic masks for foreground objects and background regions in an image.

## Getting started with mask creation

![alt image](../../assets/imagecutout-mask-example.png?raw=true "Original Image")

The `/v1/mask-objects` endpoint analyzes an input image and returns two sets of masks: `semanticMasks` for detected foreground objects, and `backgroundMasks` for background regions. Each mask includes a label, confidence score, bounding box, and a URL for the mask image.

The endpoint accepts a single input image via presigned URL. Max dimensions: 4000 x 4000 px.

Using [Example.jpg](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg), a typical cURL call might look like this:

```shell
curl -X POST \
  https://image.adobe.io/v1/mask-objects \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {
      "source": {
        "url": "<SIGNED_GET_URL>"
      }
    }
  }'
```

This initiates an asynchronous job and returns a response containing the URL to poll for job status:

```json
{
  "jobId": "e3a13d81-a462-4b71-9964-28b2ef34aca7",
  "_links": {
    "self": {
      "href": "https://image.adobe.io/v1/status/e3a13d81-a462-4b71-9964-28b2ef34aca7"
    }
  }
}
```

Using the job ID returned from the previous call, poll the `/status` href to get the job status:

```shell
curl -X GET \
  https://image.adobe.io/v1/status/e3a13d81-a462-4b71-9964-28b2ef34aca7 \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json"
```

Once the job is complete, the successful `/status` response will look similar to the following. The `semanticMasks` array contains masks for detected foreground objects, and `backgroundMasks` contains masks for background regions:

```json
{
  "jobId": "e3a13d81-a462-4b71-9964-28b2ef34aca7",
  "status": "succeeded",
  "semanticMasks": [
    {
      "label": "Person",
      "score": 0.98,
      "boundingBox": {
        "left": 120,
        "top": 45,
        "width": 320,
        "height": 610
      },
      "destination": {
        "url": "https://storage.adobe.io/..."
      },
      "mediaType": "image/png"
    }
  ],
  "backgroundMasks": [
    {
      "label": "Background",
      "score": 0.95,
      "boundingBox": {
        "left": 0,
        "top": 0,
        "width": 800,
        "height": 600
      },
      "destination": {
        "url": "https://storage.adobe.io/..."
      },
      "mediaType": "image/png"
    }
  ]
}
```
