---
title: DepthBlur
description: DepthBlur documentation
---

# DepthBlur

The DepthBlur API supports applying depth blur to your image. Depth Blur is part of the Neural Filters gallery in Photoshop. It allows you to target the area and range of blur in photos, creating wide-aperture depth of field blur effects. You may choose different focal points or remove the focal point and control the depth blur through manipulating the focal range slider. Setting focusSubject to true will select the most prominent subject in the image and apply depth blur around that subject.

You can find a code sample [here.](/guides/code_sample/index.md#applying-depth-blur-neural-filter) 

### Applying Depth Blur Neural Filter

The `depthBlur` endpoint can take an input file and apply the depth blur neural filter.

This example shows how you can apply depth blur with the appropriate parameters.

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/depthBlur \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "<storage>"
    }
  ],
  "options": {
    "haze": 25,
    "blurStrength": 30,
    "focalSelector": {
        "x": 0.22,
        "y": 0.33
    }
  },
  "outputs": [
    {
      "storage": "<storage>",
      "type": "image/jpeg",
      "href": "<SIGNED_POST_URL>"
    }
  ]
}'
```

First, be sure to follow the instructions in the [Getting Started](../../getting_started/index.md) guide to get your token.
