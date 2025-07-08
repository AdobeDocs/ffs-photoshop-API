---
title: PSD Renditions and Conversions
description: Learn how to create PSD documents and convert between different image formats using the Rendering and Conversions API endpoint
hideBreadcrumbNav: true
keywords:
  - rendering
  - conversions
  - PSD documents
  - image formats
  - document rendition
  - file conversion
contributors:
  - https://github.com/AEAbreu-hub
---

# PSD Renditions and Conversions

This endpoint allows you to create a new PSD document and renditions in different sizes.

Use this endpoint to:

* Create a new PSD document.
* Create JPEG, TIFF or PNG renditions, with various sizes.
* Request thumbnail previews of all renderable layers.
* Convert files between any of the supported file types (PSD, JPEG, TIFF, PNG).

## Creating a document rendition

This implementation example generates multiple output renditions with the API `/renditionCreate`:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/renditionCreate \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs":[
    {
      "href":"<SIGNED_GET_URL>",
      "storage":"<your_storage>"
    }
  ],
  "outputs":[
    {
      "href":"<SIGNED_POST_URL1>",          
      "width": 512,
      "storage":"<your_storage>",
      "type":"image/jpeg"      
    },
    {
      "href":"<SIGNED_POST_URL2>",
      "storage":"<your_storage>",
      "type":"image/png"
    }
  ]
}'
```

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get_job_status/).
