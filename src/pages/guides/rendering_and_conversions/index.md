---
title: Rendering and Conversions
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

# Rendering and Conversions

This endpoint allows you to create a new PSD document and various renditions of different sizes. You can also convert any supported input file format to PSD, JPEG, TIFF, or PNG.

## Getting started with rendering and conversions

This endpoint allows you to create a new PSD document and various renditions of different sizes. You can also convert any supported input file format to PSD, JPEG, TIFF, or PNG.

* Create a new PSD document.
* Create a JPEG, TIFF or PNG rendition of various sizes.
* Request thumbnail previews of all renderable layers.
* Convert between any of the supported filetypes (PSD, JPEG, TIFF, PNG).

Here is an example of creating JPEG and PNG renditions of a PSD document:
[Render PSD document][1]

### Creating a document rendition

Generate multiple output renditions with the API `renditionCreate`:

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

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to poll for the status of the job. This is illustrated in [Example 12][2] and [Example 14][3].

<!-- Links -->
[1]: /guides/code_sample/index.md#create-a-document-rendition
[2]: /guides/code_sample/index.md#fetch-the-status-of-an-api
[3]: /guides/code_sample/index.md#poll-for-job-status-for-all-other-apis
