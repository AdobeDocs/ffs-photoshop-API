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

The `/cutout` endpoint can recognize the subject of an image and eliminate the background, providing the subject as the output.

![alt image](imagecutout_cutout_example.png?raw=true "Original Image")

Use the following curl command to remove the background from an image:

```shell
curl -X POST \
  https://image.adobe.io/sensei/cutout \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
   "input":{
      "storage":"<your_storage>",
      "href":"<SIGNED_GET_URL>"
   },
   "output":{
      "storage":"<your_storage>",
      "href":"<SIGNED_POST_URL>",
      "mask":{
         "format":"soft"
      }
   }
}'
```

This initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get_job_status/).

## Customized workflow

This customized workflow is for users who'd like to generate remove background results as a Photoshop path instead of a regular mask. You'll need to chain API calls to Remove Background service and Photoshop Service.

You'll need to open the result in the Photoshop Desktop application to see the path in the path panel.

You can [download the sample end-to-end bash script][8] and follow the comments to try out this customized workflow.

Sample input and output:

* [Download the sample input file][5]
* [Download the sample output file][6]

### Steps

1. [Download the make-file.atn file][7]. This file will be used in the Photoshop action API call.
2. Make the first API call to the Remove Background service to generate an intermediate result as RGBA remove background.
3. Make the second API call to the Photoshop Action service to use the intermediate result as well as the make-file.atn file to generate a final JPEG format result with the desired Photoshop path embedded.
4. Open the final result with the Photoshop Desktop app to check the generated path in the path panel.

<!-- Links -->
[1]: /guides/code_sample/index.md#remove-background
[2]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg
[3]: /guides/code_sample/index.md#remove-background
[4]: /guides/code_sample/index.md#generate-image-mask
[5]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg
[6]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg
[7]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn
[8]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app
