---
title: Smart Objects and the API
description: Learn how to create and edit embedded Smart Objects in Photoshop files using the Smart Object API endpoint
hideBreadcrumbNav: true
keywords:
  - smart objects
  - embedded smart objects
  - PSD files
  - layer manipulation
  - image replacement
contributors:
  - https://github.com/AEAbreu-hub
---

# Smart Objects and the API

The Smart Object endpoint allows you to create and edit embedded Smart Objects in Photoshop files (PSD files). You can replace existing Smart Objects with new images while maintaining their positioning and aspect ratio, or create new Smart Objects within your document.

## Getting started with Smart Objects

The Smart Object endpoint allows you to create and edit an embedded Smart Objects in a Photoshop file, or PSD file. The Smart Object that's replaced will be positioned within the bounding box of the original image. Whether the new image is larger or smaller than the original, it will adjust to fit within the original bounding box while preserving its aspect ratio. To alter the bounds of the replaced image, you can specify bounds parameters in the API call.

### Creating a Smart Object

This example shows how you can create an embedded smart object using the `/smartObject` endpoint.

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/smartObject \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
  {
    "href": "<SIGNED_GET_URL>",
    "storage": "<storage>"
  }],
  "options": {
    "layers": [{
      "name": "New",
      "add": {
        "insertTop": true
      },
      "input": {
        "href": "<SIGNED_GET_URL>",
        "storage": "<storage>"
       }
      }
    ]
  },
  "outputs": [
  {
    "storage": "<storage>",
    "href": "<SIGNED_POST_URL>",
    "type": "vnd.adobe.photoshop"
  }
]}'
```

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to poll for the status of the job. This is illustrated in [Example, Fetch API Status][1] and [Example, Poll Job Status][2].

### Swapping the image in a smart object layer

In this example we are replacing the smartObject using `documentOperations` API

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentOperations \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs":[
    {
      "href":"<SIGNED_GET_URL>",
      "storage":"<storage>"
    }
  ],
  "options":{
    "layers":[
      {
        "edit":{},     
        "input":{                                       
          "href":"<SIGNED_GET_URL>",  
          "storage":"<storage>"
        },
        "smartObject" : {                
          "type" : "image/png"
        },
        "attributes":{
          "bounds":{
            "height":515,
            "left":-385,
            "top":-21,
            "width":929
          }
        },
        "id":750,
        "index":1,
        "locked":false,
        "name":"HeroImage",
        "type":"smartObject",
        "visible":true
      }
    ]
  },
  "outputs":[
    {
      "href":"<SIGNED_POST_URL>",
      "storage":"<storage>",
      "type":"vnd.adobe.photoshop"
    }
  ]
}'
```

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to poll for the status of the job. This is illustrated in [Example 12](/guides/code_sample/index.md#fetch-the-status-of-an-api) and [Example 14](/guides/code_sample/index.md#poll-for-job-status-for-all-other-apis)

### Known limitations

* If your document contains transparent pixels, (e.g some .png), you may not get consistent bounds.
* We currently don't support Linked Smart Objects.
* In order to update an embedded Smart Object that is referenced by multiple layers you need to update each of those layers in order for the Smart Object to be replaced in those layers.

Here is an example of replacing a Smart Object within a layer:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/smartObject \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
  {
    "href": "<SIGNED_GET_URL>",
    "storage": "<storage>"
  }],
  "options": {
    "layers": [{
      "name": "HeroImage",
      "input": {
        "href": "<SIGNED_GET_URL>",
        "storage": "<storage>"
      }
     }
    ]
  },
  "outputs": [
  {
    "storage": "<storage>",
    "href": "<SIGNED_POST_URL>",
    "type": "vnd.adobe.photoshop"
  }
]}'
```

For better performance, we rasterize our smart objects that are bigger than 2000 pixels * 2000 pixels.
For optimal processing, please make sure the embedded smart object that you want to replace only contains alphanumeric characters in its name.

In this example, we generated a Smart Object within the "socks" layer and utilized the API to substitute the original image with a new pattern. This process facilitated the creation of two variations of the identical photograph.

![alt image](smartobject_example.png?raw=true "Original Image")

<!-- Links -->
[1]: ../../guides/code_sample/index.md#fetch-the-status-of-an-api
[2]: ../../guides/code_sample/index.md#poll-for-job-status-for-all-other-apis 