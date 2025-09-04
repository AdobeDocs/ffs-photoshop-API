---
title: Remove Background
description: Learn how to use the Remove Background API to automatically detect and remove backgrounds from images while preserving the main subject
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

<InlineAlert variant="warning" slots="header, text" />

V1 is deprecated.

The Remove Background V1 API (https://image.adobe.io/sensei/cutout) is deprecated. Although these workflow examples use the `/cutout` endpoint, any current implementations should migrate to Remove Background V2 API (https://image.adobe.io/v2/remove-background) by referring to [the V2 migration instructions below][1] to avoid interruptions.

The `/cutout` endpoint can recognize the subject of an image and eliminate the background, providing the subject as the output.

![alt image](imagecutout_cutout_example.png?raw=true "Original Image")

Use the following cURL command to remove the background from an image:

```shell
curl -X POST \
  https://image.adobe.io/sensei/cutout \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
   "input":{
      "storage":"<your_storage>",
      "href":"<signed_get_url>"
   },
   "output":{
      "storage":"<your_storage>",
      "href":"<signed_post_url>",
      "mask":{
         "format":"soft"
      }
   }
}'
```

This initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job][2].

## Customized workflow

This customized workflow is for users who'd like to generate remove background results as a Photoshop path instead of a regular mask. You'll need to chain API calls to Remove Background service and Photoshop Service.

You'll need to open the result in the Photoshop Desktop application to see the path in the path panel.

You can [download the sample end-to-end bash script][3] and follow the comments to try out this customized workflow.

Sample input and output:

* [Download the sample input file][4].
* [Download the sample output file][5].

### Implementation steps

1. [Download the make-file.atn file][6]. This file will be used in the Photoshop action API call.
2. Make the first API call to the Remove Background service to generate an intermediate result as RGBA remove background.
3. Make the second API call to the Photoshop Action service to use the intermediate result as well as the make-file.atn file to generate a final JPEG format result with the desired Photoshop path embedded.
4. Open the final result with the Photoshop Desktop app to check the generated path in the path panel.

## Migrating to Remove Background V2

The Remove Background V1 API (https://image.adobe.io/sensei/cutout) used in these example workflows is deprecated. To avoid service interruptions, migrate to Remove Background V2 API (https://image.adobe.io/v2/remove-background) by referring to these steps and considerations.

### Step 1: Update the endpoint and payload

Update your Remove Background endpoint from `/sensei/cutout` to `/v2/remove-background`.

**V1 Payload:**

```shell
curl -i -X POST \
  https://image.adobe.io/sensei/cutout \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_API_KEY_HERE' \
  -H 'x-gw-ims-org-id: string' \
  -d '{
    "input": {
      "href": "string",
      "storage": "external"
    },
    "output": {
      "href": "string",
      "storage": "external",
      "mask": {
        "format": "binary"
      },
      "color": {
        "space": "rgb"
      },
      "overwrite": true
    }
  }'
```

**V2 Payload:**

```shell
curl -i -X POST \
  https://image.adobe.io/v2/remove-background \
  -H 'Authorization: string' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_API_KEY_HERE' \
  -d '{
    "image": {
      "source": {
        "url": "string"
      }
    },
    "mode": "cutout",
    "output": {
      "mediaType": "image/jpeg"
    },
    "trim": false,
    "backgroundColor": {
      "red": 255,
      "green": 255,
      "blue": 255,
      "alpha": 1
    },
    "colorDecontamination": 1
  }'
```

### Step 2: Test your integration

Be sure to:

* Run your workflow against the V2 endpoint.

* Check that the outputs are correct; V2 includes improved post-processing for cleaner edges and reduced matting.

### Step 3: Deploy the change

To deploy the change:

* Update production systems with the V2 endpoint and payload.

* Monitor results for any errors or issues.

### Notes for developers

Be aware that the V2 endpoint uses a slightly different payload structure.
Ensure that `image.source.url` and `output.mediaType` are set correctly.

Optional parameters like `trim` and `colorDecontamination` are available in V2 for enhanced output quality.

The latest technical information is always available on [the API reference documentation][7].

For support, contact your Adobe Customer Success Manager.

<!-- Links -->
[1]: #migrating-to-remove-background-v2
[2]: /guides/get_job_status/
[3]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app
[4]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg
[5]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg
[6]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn
[7]: https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground

