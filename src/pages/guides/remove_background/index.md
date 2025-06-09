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

The Remove Background endpoint can recognize the primary subject within an image and eliminate the background, providing the subject as the output. This API uses advanced AI to automatically detect and isolate the main subject from any background.

## Getting started with background removal

The Remove Background endpoint can recognize the primary subject within an image and eliminate the background, providing the subject as the output. You can see a code sample [here][1].

Example of Remove Background with a sample image:

![alt image](imagecutout_cutout_example.png?raw=true "Original Image")

The `/cutout` API takes a single input image to generate your mask or remove background from. Using [Example.jpg][2], a typical curl call might look like this:

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

This initiates an asynchronous job and returns a response containing the href to poll for job status and the JSON manifest.

```json
{
    "_links": {
        "self": {
            "href": "https://image.adobe.io/sensei/status/e3a13d81-a462-4b71-9964-28b2ef34aca7"
        }
    }
}
```

Using the job ID returned from the previous call you can poll on the returned `/status` href to get the job status:

```shell
curl -X GET \
  https://image.adobe.io/sensei/status/e3a13d81-a462-4b71-9964-28b2ef34aca7 \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json"
```

Once the job is complete your successful `/status` response will look similar to the response below. The output will have been placed in your requested location. In the event of failure the errors will be shown instead:

```json
{
    "jobID": "e3a13d81-a462-4b71-9964-28b2ef34aca7",
    "status": "succeeded",
    "created": "2020-02-11T21:08:43.789Z",
    "modified": "2020-02-11T21:08:48.492Z",
    "input": "<SIGNED_GET_URL>",
    "_links": {
        "self": {
            "href": "https://image.adobe.io/sensei/status/e3a13d81-a462-4b71-9964-28b2ef34aca7"
        }
    },
    "output": {
        "storage": "<your_storage>",
        "href": "<SIGNED_POST_URL>",
        "mask": {
            "format": "soft"
        }
    }
}
```

## Customized workflow

### Generating remove background result as Photoshop path

This workflow is ONLY for users who'd like to generate remove background result as Photoshop path instead of regular mask or remove background in above [example 1][3] and [example 2][4]. You will need to chain API calls to Remove Background service and Photoshop Service to achieve this goal.

#### Sample input/output

Sample input from [here][5].
Sample output from [here][6] (Note: you will need to open result in Photoshop Desktop application so that you will see the path in path panel).

#### Instructions

1. Download the make-file.atn file from [here][7] (this file will be used in the Photoshop action API call).
2. Make the first API call to Remove Background service to generate intermediate result as RGBA remove background.
3. Make the second API call to Photoshop action service to use above intermediate result as well as the make-file.atn file to generate final JPEG format result with desired PS path embedded.
4. Open the final result with Photoshop Desktop app to check generated path in path panel.

#### Sample code

You can download the sample end-to-end bash script [here][8] and then follow the comments to try it out this customized workflow.

<!-- Links -->
[1]: /guides/code_sample/index.md#remove-background
[2]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg
[3]: /guides/code_sample/index.md#remove-background
[4]: /guides/code_sample/index.md#generate-image-mask
[5]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg
[6]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg
[7]: https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn
[8]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app