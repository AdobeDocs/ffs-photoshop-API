---
title: Getting started with Smart Objects
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

# Getting started with Smart Objects

The Smart Object endpoint allows you to create and edit an embedded Smart Object in a PSD file.

The Smart Object that is replaced will be positioned within the bounding box of the original image. Whether the new image is larger or smaller than the original, it will adjust to fit within the original bounding box while preserving its aspect ratio. To alter the bounds of the replaced image, you can specify bounds parameters in the API call.

For these example images, we generated a Smart Object within the "socks" layer and used the API to substitute the original image with a new pattern, creating two variations of the identical photograph.

![alt image](../../assets/smartobject-example.png?raw=true "Original Image")

## Known limitations

* If your document contains transparent pixels, (e.g some .png), you may not get consistent bounds.
* We currently don't support Linked Smart Objects.
* In order to update an embedded Smart Object that is referenced by multiple layers you need to update each of those layers in order for the Smart Object to be replaced in those layers.
* For better performance, we rasterize our smart objects that are bigger than 2000x2000 pixels.For optimal processing, make sure the embedded smart object that you want to replace only contains alphanumeric characters in its name.

## Implementation examples

### Creating a Smart Object

This example creates an embedded smart object using the `/smartObject` endpoint.

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

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get-job-status/index.md).

### Swapping the image in a smart object layer

In this example we're replacing the smartObject using the `documentOperations` API.

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

A call to this API initiates an asynchronous job and returns a response containing an href. Use the value in the href to [poll for the status of the job](/guides/get-job-status/index.md).

### Replacing a Smart Object within a layer

This example replaces a Smart Object within a layer.

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

## Opening the output PSD in Photoshop

When you open the output PSD locally in Photoshop, you may see a **"missing file"** prompt for the linked smart object. This is expected behavior, not a bug. The path stored inside the PSD points to the server location where the file resided during processing — that path will not resolve on your local machine. Photoshop is correctly flagging the broken link.

You have two options depending on your workflow:

1. **Relink locally.** Keep a copy of the source asset (the file you passed as the linked smart object) somewhere accessible on your machine. In Photoshop, use the **Layer** panel → **Smart Objects** → **Relink to File**,

   ![Relinking the smart object in Photoshop](../../assets/relink-2.jpg?raw=true "Relinking the smart object")

   or respond to the missing-link dialog when the PSD opens. Once relinked, Photoshop will remember the new path.

   ![Missing file prompt in Photoshop](../../assets/relink-1.jpg?raw=true "Missing file prompt")

2. **Use embedded smart objects instead.** If portability matters more than the linked-asset workflow — for example, when handing off the PSD to an end user who just wants to open and work without managing external files — embedded smart objects travel with the PSD and eliminate the relinking step. Set `"isLinked": false` (or omit `isLinked`) in the `smartObject` block to embed rather than link. Linked smart objects are the right choice when you manage your own asset pipeline and want explicit control over source files; embedded is generally smoother for hand-off scenarios.

