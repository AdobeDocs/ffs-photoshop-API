---
title: Remove Background
description: Remove Background documentation
---

# Remove Background

The Remove Background endpoint can recognize the primary subject within an image and eliminate the background, providing the subject as the output. You can see a code sample [here.](/guides/code_sample/index.md#remove-background).<br />

Example of Remove Background with a sample image.
![alt image](imagecutout_cutout_example.png?raw=true "Original Image") 


The `/cutout` api takes a single input image to generate your mask or remove background from. Using [Example.jpg](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg), a typical curl call might look like this:

```shell
curl -X POST \
  https://image.adobe.io/sensei/cutout \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
   "input":{
      "storage":"<storage>",
      "href":"<SIGNED_GET_URL>"
   },
   "output":{
      "storage":"<storage>",
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

Using the job id returned from the previous call you can poll on the returned `/status` href to get the job status

```shell
curl -X GET \
  https://image.adobe.io/sensei/status/e3a13d81-a462-4b71-9964-28b2ef34aca7 \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json"
```

Once the job is complete your successful `/status` response will look similar to the response below; The output will have been placed in your requested location. In the event of failure the errors will be shown instead

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
        "storage": "<storage>",
        "href": "<SIGNED_POST_URL>",
        "mask": {
            "format": "soft"
        }
    }
}
```

## Customized Workflow

### Generate Remove Background result as Photoshop path

This workflow is ONLY for users who'd like to generate remove background result as Photoshop path instead of regular mask or remove background in above [example 1](/guides/code_sample/index.md#remove-background) and [example 2](/guides/code_sample/index.md#generate-image-mask). You will need to chain API calls to Remove Background service and Photoshop Service to achieve this goal.

#### Sample Input/Output

Sample input from [here](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/input.jpg).
Sample output from [here](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/result_with_path.jpg) (Note: you will need to open result in Photoshop Desktop application so that you will see the path in path panel)

#### Instructions

1. Download the make-file.atn file from [here](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/ic_customized_workflow/make-path.atn) (this file will be used in the Photoshop action API call)
2. Make the first API call to Remove Background service to generate intermediate result as RGBA remove background
3. Make the second API call to Photoshop action service to use above intermediate result as well as the make-file.atn file to generate final JPEG format result with desired PS path embedded
4. Open the final result with Photoshop Desktop app to check generated path in path panel

#### Sample Code

You can download the sample end-to-end bash script [here](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/ic-customized-workflow-app) and then follow the comments to try it out this customized workflow.