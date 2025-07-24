---
title: Applying a Depth Blur
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

The Depth Blur API supports applying depth blur to your image.

Depth Blur is part of the Neural Filters gallery in Photoshop. It allows you to target the area and range of blur in photos, creating wide-aperture depth of field blur effects.

You may choose different focal points or remove the focal point and control the depth blur through manipulating the focal range slider. Setting `focusSubject` to `true` will select the most prominent subject in the image and apply depth blur around that subject.

## Applying depth blur neural filter

This implementation example shows how to apply depth blur with the appropriate parameters:

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
