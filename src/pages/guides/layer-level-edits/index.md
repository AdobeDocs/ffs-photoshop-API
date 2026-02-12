---
title: Layer Level Edits
description: Learn how to perform layer-level edits in Photoshop files including adding, editing, and deleting layers, adjustment layers, and pixel layers
hideBreadcrumbNav: true
keywords:
  - layer edits
  - adjustment layers
  - pixel layers
  - shape layers
  - document operations
  - PSD editing
contributors:
  - https://github.com/AEAbreu-hub
---

# Layer level edits

Perform various operations on layers within Photoshop files, including adding, editing, and deleting layers, working with adjustment layers, pixel layers, and shape layers.

## Adding, editing and deleting layers

Use the `/documentOperations` API to make layer and/or document level edits to your PSD and then generate new renditions with the changes.

You can pass in a flat array of only the layers that you wish to act upon, in the `options.layers` argument of the request body. Use the layer ID to identify the correct layers in your PSD.

The `add`, `edit`, `move` and `delete` blocks indicate the action to be taken on a layer object. Any layer block that's missing one of these attributes will be ignored.

The `add` and `move` blocks must also supply one of the attributes `insertAbove`, `insertBelow`, `insertInto`, `insertTop` or `insertBottom` to indicate where to move the layer.

Adding a new layer doesn't require the inclusion of a layer ID. The service will generate a new layer ID.

## Implementation examples

### Making an edit to a layer

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/documentOperations \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs":[
    {
      "href":"<your_signed_get_url>",
      "storage":"<your_storage>"
    }
  ],
  "options":{
    "layers":[
      {
        "edit":{},    
        "id":750,
        "index":1,
        "locked":true,
        "name":"HeroImage",
        "type":"smartObject",
        "visible":true
      }
    ]
  },
  "outputs":[
    {
      "href":"<your_signed_post_url>",
      "storage":"<your_storage>",
      "type":"vnd.adobe.photoshop"
    }
  ]
}'
```

### Adding a new adjustment layer

This example shows how to add a new `brightnessContrast` adjustment layer to the top of your PSD:

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
        "add":{                             
          "insertAbove": {
            "id": 549
          }                   
        },
        "adjustments":{
          "brightnessContrast":{
            "brightness":25,
            "contrast":-40
          }
        },
        "name":"NewBrightnessContrast",
        "type":"adjustmentLayer"             
      }
    ]
  },
  "outputs":[
    {
      "href":"<SIGNED_POST_URL>",
      "storage":"<storage>",
      "type":"image/jpeg"
    }
  ]
}'
```

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get_job_status/).

### Editing a pixel layer

In this example we replace the image in an existing pixel layer, the `Hero Image` layer in `Example.psd`:

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
      "storage":"<your_storage>"
    }
  ],
  "options":{
    "layers":[
      {
        "edit":{},                   
        "input":{                                      
          "href":"<SIGNED_GET_URL>",
          "storage":"<your_storage>"
        },
        "bounds":{
          "height":405,
          "left":0,
          "top":237,
          "width":300
        },
        "id":751,
        "index":2,
        "locked":false,
        "name":"BackgroundGradient",
        "type":"layer",
        "visible":true
      }
    ]
  },
  "outputs":[
    {
      "href":"<SIGNED_POST_URL>",
      "storage":"<your_storage>",
      "type":"vnd.adobe.photoshop"
    }
  ]
}'
```

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get_job_status/).
