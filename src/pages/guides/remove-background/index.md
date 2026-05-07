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

The `/v2/remove-background` endpoint can recognize the subject of an image and eliminate the background, providing the subject as the output.

![alt image](../../assets/imagecutout-cutout-example.png?raw=true "Original Image")

Use the following cURL command to remove the background from an image:

```shell
curl -i -X POST \
  https://image.adobe.io/v2/remove-background \
  -H 'Authorization: Bearer $token' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: $apiKey' \
  -d '{
    "image": {
      "source": {
        "url": "<signed_get_url>"
      }
    },
    "mode": "cutout",
    "output": {
      "mediaType": "image/png"
    }
  }'
```

This initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get-job-status/index.md).

## Customized workflow

This customized workflow is for users who'd like to generate remove background results as a Photoshop path instead of a regular mask. You'll need to chain API calls to Remove Background service and Photoshop Service.

You'll need to open the result in the Photoshop Desktop application to see the path in the path panel.

You can [download the sample end-to-end bash script](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app) and follow the comments to try out this customized workflow.

Sample input and output:

* [Download the sample input file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg).
* [Download the sample output file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg).

### Implementation steps

1. [Download the make-file.atn file](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn). This file will be used in the Photoshop action API call.
2. Make the first API call to the Remove Background service to generate an intermediate result as RGBA remove background.
3. Make the second API call to the Photoshop Action service to use the intermediate result as well as the make-file.atn file to generate a final JPEG format result with the desired Photoshop path embedded.
4. Open the final result with the Photoshop Desktop app to check the generated path in the path panel.

## Optional parameters

The V2 endpoint supports additional parameters for enhanced output quality:

| Parameter | Type | Description |
| --- | --- | --- |
| `mode` | string | Output mode. `cutout` returns the subject on a transparent background; `mask` returns a grayscale mask. |
| `trim` | boolean | Trims transparent edges from the output image. |
| `backgroundColor` | object | Sets a background fill color (RGBA). |
| `colorDecontamination` | number | Reduces color bleed from the removed background (0–1). |

For the latest technical information, see [the API reference documentation](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground).

For support, contact your Adobe Customer Success Manager.
