---
title: Depth Blur
description: Learn how to apply depth blur effects to images using the Depth Blur API endpoint with neural filter technology
hideBreadcrumbNav: true
keywords:
  - depth blur
  - neural filters
  - depth of field
  - focal point
  - image blur
contributors:
  - https://github.com/AEAbreu-hub
---

# Depth Blur

The Depth Blur API supports applying depth blur to your image. Depth Blur is part of the Neural Filters gallery in Photoshop. It allows you to target the area and range of blur in photos, creating wide-aperture depth of field blur effects.

## Getting started with depth blur

The Depth Blur API supports applying depth blur to your image. Depth Blur is part of the Neural Filters gallery in Photoshop. It allows you to target the area and range of blur in photos, creating wide-aperture depth of field blur effects. You may choose different focal points or remove the focal point and control the depth blur through manipulating the focal range slider. Setting focusSubject to true will select the most prominent subject in the image and apply depth blur around that subject.

You can find a code sample [here][1].

### Applying depth blur neural filter

The `depthBlur` endpoint can take an input file and apply the depth blur neural filter.

This example shows how you can apply depth blur with the appropriate parameters:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/depthBlur \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<your_signed_get_url>",
      "storage": "<your_storage>"
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
      "storage": "<your_storage>",
      "type": "image/jpeg",
      "href": "<your_signed_post_url>"
    }
  ]
}'
```

First, be sure to follow the instructions in the [Getting Started][2] guide to get your token.

<!-- Links -->
[1]: /guides/code_sample/index.md#applying-depth-blur-neural-filter
[2]: ../../getting_started/index.md
