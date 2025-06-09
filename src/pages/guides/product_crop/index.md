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
---

# Product Crop

The Product Crop endpoint facilitates smart cropping for images, automatically detecting the subject and ensuring it remains the focal point of the cropped image. You can identify the product and specify the desired padding for your cropped image.

## Getting started with product cropping

The Product Crop endpoint facilitates smart cropping for images, automatically detecting the subject and ensuring it remains the focal point of the cropped image. You can identify the product and specify the desired padding for your cropped image. You can see some sample code [here][1].

### Applying product crop

The `productCrop` endpoint can take an input file and apply right crop to it. We don't support multilayered PSD.

This example shows how you can apply the crop with required padding to an input file:

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
    "padding": {
      "unit": "Pixels",
      "width": 10,
      "height": 10
    }
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

### Known limitations

The current model is trained to return a crop that respects the salient object within an image. There is a current known issue that when a person or portrait is contained within a salient object, the model will crop with the person as the focal area rather than the salient object that contains it. This is problematic in the case of an item where an image of a person is contained within a design (i.e. a t-shirt, collectible or art). Rather than crop to the intended item, the service will crop to the person within the item.

We intend to correct this issue in future releases.

<!-- Links -->
[1]: /guides/code_sample/index.md#applying-product-crop 