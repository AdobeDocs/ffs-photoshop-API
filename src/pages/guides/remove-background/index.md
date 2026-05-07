---
title: Firefly's Remove Background API Feature Guide
description: Learn how to use the Remove Background API to automatically detect and remove backgrounds from images while preserving the main subject.
hideBreadcrumbNav: true
keywords:
  - remove background
  - background removal
  - image cutout
  - subject detection
  - mask generation
contributors:
  - https://github.com/AEAbreu-hub
---

# Remove Background

This API uses advanced AI to automatically detect and isolate the main subject of an image and remove the background.

## Overview

Use **Remove Background v2**: submit a job with `POST https://image.adobe.io/v2/remove-background`, then poll **`GET https://image.adobe.io/v2/status/{jobId}`** with the `jobId` from the response until the job completes. See [Remove background](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground) and [Get status - v2](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/facadeJobStatus) in the API reference.

The following example removes the background (cutout-style output) using an external image URL:

![alt image](../../assets/imagecutout-cutout-example.png?raw=true "Original Image")

```shell
curl -X POST \
  https://image.adobe.io/v2/remove-background \
  -H "Authorization: Bearer $token" \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
    "image": {
      "source": {
        "url": "<signed_get_url_or_supported_source_url>"
      }
    },
    "mode": "cutout",
    "output": {
      "mediaType": "image/png"
    }
  }'
```

The response includes `jobId` and `statusUrl`. Poll `statusUrl`, or call `GET https://image.adobe.io/v2/status/{jobId}` with that `jobId`, until `status` is `succeeded` or `failed`.

## Customized workflow

This customized workflow is for users who'd like to generate remove background results as a Photoshop path instead of a regular mask. You'll need to chain API calls to Remove Background service and Photoshop Service.

You'll need to open the result in the Photoshop Desktop application to see the path in the path panel.

You can [download the sample end-to-end bash script](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app) and follow the comments to try out this customized workflow.

Sample input and output:

* [Download the sample input file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg).
* [Download the sample output file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg).

### Implementation steps

1. [Download the make-file.atn file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn). This file will be used in the Photoshop action API call.
2. Make the first API call to Remove Background v2 to generate an intermediate result as RGBA remove background.
3. Make the second API call to the Photoshop Action service to use the intermediate result as well as the make-file.atn file to generate a final JPEG format result with the desired Photoshop path embedded.
4. Open the final result with the Photoshop Desktop app to check the generated path in the path panel.

## Migrating from legacy Sensei endpoints

The legacy `/sensei/cutout`, `/sensei/mask`, and `/sensei/status/{jobId}` flows are **not** included in the current Photoshop API OpenAPI reference. Integrations should use **`POST /v2/remove-background`** and **`GET /v2/status/{jobId}`** instead.

* Use **`mode`: `"cutout"`** for subject cutout output, **`mode`: `"mask"`** for a grayscale mask PNG, or **`mode`: `"psd"`** when you need PSD output (see the reference schema for `RemoveBgMode`).
* Request bodies use the v2 shape (`image.source.url`, optional `output.mediaType`, `trim`, `backgroundColor`, `colorDecontamination`, and so on)—not the older `input` / `output` storage objects used by Sensei.

For deprecation timelines and support, see [Deprecation Announcement](/getting-started/deprecation-announcement/index.md) and [Remove background](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground) in the API reference.
