---
title: Create a mask
description: Learn how to create grayscale mask PNG files using Remove Background v2 (mask mode) for image compositing and editing
hideBreadcrumbNav: true
keywords:
  - create mask
  - image mask
  - grayscale mask
  - mask generation
  - image compositing
contributors:
  - https://github.com/AEAbreu-hub
---

# Create Mask

Create a grayscale mask that you can composite onto the original image using **Remove Background v2** with **`mode` set to `"mask"`**.

## Overview

The Remove Background service returns a PNG mask around the subject when you use `"mode": "mask"`. Submit `POST https://image.adobe.io/v2/remove-background`, then poll **`GET https://image.adobe.io/v2/status/{jobId}`** until the job completes. See [Remove background](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground) and [Get status - v2](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/facadeJobStatus).

![alt image](../../assets/imagecutout-mask-example.png?raw=true "Original Image")

Using [Example.jpg](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg), a typical flow looks like this:

**1. Start the job**

```shell
curl -X POST \
  https://image.adobe.io/v2/remove-background \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {
      "source": {
        "url": "<SIGNED_GET_URL_OR_SUPPORTED_SOURCE_URL>"
      }
    },
    "mode": "mask",
    "output": {
      "mediaType": "image/png"
    }
  }'
```

The **202** response includes `jobId` and `statusUrl`. For example:

```json
{
  "jobId": "urn:ff:jobs:YOUR_JOB_ID",
  "statusUrl": "https://image.adobe.io/v2/status/urn:ff:jobs:YOUR_JOB_ID"
}
```

**2. Poll for status**

Use `statusUrl`, or call:

```shell
curl -X GET \
  "https://image.adobe.io/v2/status/urn:ff:jobs:YOUR_JOB_ID" \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey"
```

When `status` is `succeeded`, the payload includes `result.outputs` with URLs for the generated mask file (shape matches [Get status - v2](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/facadeJobStatus) in the API reference). If the job `failed`, error details appear in the status payload.

For subject cutout (RGBA) instead of a grayscale mask, use `"mode": "cutout"`. See also [Remove background](/guides/remove-background/index.md).
