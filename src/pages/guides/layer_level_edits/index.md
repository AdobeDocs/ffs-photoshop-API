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

# Layer Level Edits

## Overview

The Layer Level Edits API allows you to perform various operations on layers within Photoshop files, including adding, editing, and deleting layers, as well as working with adjustment layers, pixel layers, and shape layers.

## Getting started with layer editing

* General layer edits
  * Edit the layer name.
  * Toggle the layer locked state.
  * Toggle layer visibility.
  * Move or resize the layer via its bounds.
  * Delete layers.
* Adjustment layers
  * Add or edit an adjustment layer. The following types of adjustment layers are currently supported:
    * Brightness and Contrast.
    * Exposure.
    * Hue and Saturation.
    * Color Balance.
* Image/Pixel layers
  * Add a new pixel layer, with optional image.
  * Swap the image in an existing pixel layer.
* Shape layers
  * Resize a shape layer via its bounds.

### Adding, editing and deleting layers

The `/documentOperations` API should primarily be used to make layer and/or document level edits to your PSD and then generate new renditions with the changes. You can pass in a flat array of only the layers that you wish to act upon, in the `options.layers` argument of the request body.
The layer name (or the layer id) will be used by the service to identify the correct layer to operation upon in your PSD.

The `add`, `edit`, `move` and `delete` blocks indicate the action you would like to be taken on a particular layer object. Any layer block passed into the API that is missing one of these attributes will be ignored.
The `add` and `move` blocks must also supply one of the attributes `insertAbove`, `insertBelow`, `insertInto`, `insertTop` or `insertBottom` to indicate where you want to move the layer to. More details on this can be found in the API reference.

**Note**: Adding a new layer doesn't require the ID to be included, the service will generate a new layer id for you.

Here are some examples of making various layer level edits.

* [Layer level editing][1]

### Making a simple edit

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

* [Adding a new Adjustment Layer][2]

### Adding a new adjustment layer

This example shows how you can add a new brightnessContrast adjustment layer to the top of your PSD:

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

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to poll for the status of the job. This is illustrated in [Example 12][3] and [Example 14][4].

* [Editing Image in a Pixel Layer][5]

### Editing a pixel layer

In this example we want to replace the image in an existing pixel layer, the Hero Image layer in Example.psd:

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

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to poll for the status of the job. This is illustrated in [Example 12][3] and [Example 14][4].

<!-- Links -->
[1]: /guides/code_sample/index.md#making-a-simple-edit
[2]: /guides/code_sample/index.md#adding-a-new-adjustment-layer
[3]: /guides/code_sample/index.md#fetch-the-status-of-an-api
[4]: /guides/code_sample/index.md#poll-for-job-status-for-all-other-apis
[5]: /guides/code_sample/index.md#editing-a-pixel-layer
