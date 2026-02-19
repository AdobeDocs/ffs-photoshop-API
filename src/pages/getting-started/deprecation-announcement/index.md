---
title: Deprecation Announcement
description: Learn about the deprecation of the Photoshop API.
hideBreadcrumbNav: true
keywords:
  - deprecation
  - photoshop api
---

# Deprecation announcement

The Remove Background V1 API (`/sensei/cutout`) and the Mask API (`/sensei/mask`) are being deprecated in favor of the Remove Background V2 API (`/v2/remove-background`).

Remove Background V2 now supports both cutout and mask workflows through a single endpoint. The Remove Background V1 API and Mask API will reach End of Life (EOL) on *October 15, 2025*. After this date, they will no longer be supported or accessible.
Please begin migration to Remove Background V2 as soon as possible to ensure uninterrupted service.

For guidance about this change, refer to the FAQs below.

<AccordionItem slots="heading, text" />

### What should I do?

Migrate to the Remove Background V2 API before **October 15, 2025** to avoid service disruptions. \<br /\>  
Remove Background V2 now handles both cutout and mask workflows using a single endpoint. To specify which operation you want, set the `"mode"` parameter in your request to `"cutout"` for background removal or `"mask"` for generating a mask. This allows a single API to support both workflows while ensuring consistent, high-quality results.

<AccordionItem slots="heading, text" />

### Why is Adobe making this change?

We're moving to the Remove Background V2 API because it delivers: \<br /\> \<br /\> - Cleaner cutouts - The improved post-processing reduces matting and creates sharper edges. \<br /\> - Higher quality automation - Outputs with V2 are optimized for production pipelines and automated workflows.  \<br /\> - Ongoing support - V2 is the actively supported service that will receive updates and improvements.

<AccordionItem slots="heading, text" />

### When is this happening?

Deprecation Notice: September 2, 2025. \<br /\>
End of Life (EOL): October 15, 2025.

<AccordionItem slots="heading, text" />

### Where can I find resources?

The latest comprehensive [information about all Photoshop APIs is available on the API Reference page](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground). \<br /\> \<br /\>
For technical details specifically about the Remove Background V2 API, refer to the [Remove Background V2 endpoint](https://image.adobe.io/v2/remove-background).

<AccordionItem slots="heading, text"/>

### Who can help me with migration?

Your Adobe Customer Success Manager and Support Team are available to answer questions and guide you through the transition.

<AccordionItem slots="heading, text, code" />

### Can I see any newer example cutout request?

**Cutout workflow**

```shell
curl -i -X POST \
  https://image.adobe.io/v2/remove-background \
  -H 'Authorization: string' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_API_KEY_HERE' \
  -d '{
    "image": {
      "source": {
        "url": "string"
      }
    },
    // Set "mode:" to "cutout" for background removal
    "mode": "cutout",  
    "output": {
      "mediaType": "image/jpeg"
    },
    "trim": false,
    "backgroundColor": {
      "red": 255,
      "green": 255,
      "blue": 255,
      "alpha": 1
    },
    "colorDecontamination": 1
  }'
```

<AccordionItem slots="heading, text, code" />

### Can I see a newer example mask request?

**Mask workflow**

```shell
curl -i -X POST \
  https://image.adobe.io/v2/remove-background \
  -H 'Authorization: string' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_API_KEY_HERE' \
  -d '{
    "image": {
      "source": {
        "url": "string"
      }
    },
    // Set "mode:" to "mask" to generate a mask of the subject
    "mode": "mask",  
    "output": {
      "mediaType": "image/png"
    },
    "trim": false,
    "backgroundColor": {
      "red": 255,
      "green": 255,
      "blue": 255,
      "alpha": 1
    },
    "colorDecontamination": 1
  }'
```
