---
title: Product Crop
description: Learn how to use the Product Crop endpoint to automatically detect and crop images while keeping the subject as the focal point
hideBreadcrumbNav: true
keywords:
  - product crop
  - smart cropping
  - image cropping
  - subject detection
  - automatic cropping
contributors:
  - https://github.com/AEAbreu-hub
---

# Product Crop

The Product Crop endpoint facilitates smart cropping for images, automatically detecting the subject and ensuring it remains the focal point.

The `/productCrop` endpoint can take an input file and crop it. It doesn't support multilayered PSD files.

### Known limitations

There is a known issue when a figure or portrait is present in the design on a salient object (like a t-shirt, collectible or artwork). In these cases the model will sometimes perform a crop with the figure as the focal area rather than the object itself.

## Implementation example

This example shows how to apply the crop to an input file:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/productCrop \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "<your_storage>"
    }
  ],
  "options": {
    "unit": "Pixels",
    "width": 0,
    "height": 0
  },
  "outputs": [
    {
      "storage": "<your_storage>",
      "type": "image/jpeg",
      "href": "<SIGNED_POST_URL>"
    }
  ]
}'
```
