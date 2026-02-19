---
title: Create a mask
description: Learn how to create grayscale mask PNG files using the Create Mask API endpoint for image compositing and editing
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

Create a grayscale mask that you can composite onto the original image.

## Getting started with mask creation

![alt image](../../assets/imagecutout-mask-example.png?raw=true "Original Image")

The `/mask` endpoint allows you to create a grayscale mask PNG file that you can composite onto the original image (or any other). The mask provides precise control over which parts of an image are affected by any subsequent operations.

The endpoint accepts a single input image to generate your mask.

Using [Example.jpg](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.jpg), a typical cURL call might look like this:

```shell
curl -X POST \
  https://image.adobe.io/sensei/mask \
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

This initiates an asynchronous job and returns a response containing the URL to poll for job status and the JSON manifest.

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
