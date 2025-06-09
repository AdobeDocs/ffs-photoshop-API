---
title: Product Crop
description: Product Crop documentation
---

# Product Crop

The Product Crop endpoint facilitates smart cropping for images, automatically detecting the subject and ensuring it remains the focal point of the cropped image. You can identify the product and specify the desired padding for their cropped image. You can see some sample code [here](/guides/code_sample/index.md#applying-product-crop).

### Known Limitations

The current model is trained to return a crop that respects the salient object within an image. There is a current known issue that when a person or portrait is contained within a salient object, the model will crop with the person as the focal area rather than the salient object that contains it. This is problematic in the case of an item where an image of a person is contained within a design (i.e. a t-shirt, collectible or art). Rather than crop to the intended item, the service will crop to the person within the item.
We intend to correct this issue in future releases. 