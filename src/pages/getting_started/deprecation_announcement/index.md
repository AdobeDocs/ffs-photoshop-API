---
title: Deprecation Announcement
description: Learn about the deprecation of the Photoshop API.
hideBreadcrumbNav: true
keywords:
  - deprecation
  - photoshop api
---

# Deprecation Announcement

The Remove Background V1 API (`https://image.adobe.io/sensei/cutout`) and the Mask API (`https://image.adobe.io/sensei/mask`) are being deprecated in favor of the Remove Background V2 API (`https://image.adobe.io/v2/remove-background`).

Remove Background V2 now supports both cutout and mask workflows through a single endpoint. The Remove Background V1 API and Mask API will reach End of Life (EOL) on *October 15, 2025*. After this date, they will no longer be supported or accessible.  
Please begin migration to Remove Background V2 as soon as possible to ensure uninterrupted service.

For guidance about this change, refer to the FAQs below.

<Accordion>

<AccordionItem header="What Should I Do?" isChevronIcon position="right" iconColor="#1473E6">

Migrate to the Remove Background V2 API before **October 15, 2025** to avoid service disruptions.  

Remove Background V2 now handles both cutout and mask workflows using a single endpoint. To specify which operation you want, set the `"mode"` parameter in your request to `"cutout"` for background removal or `"mask"` for generating a mask. This allows a single API to support both workflows while ensuring consistent, high-quality results.

</AccordionItem>

<AccordionItem header="Why Is Adobe Making This Change?" isChevronIcon position="right" iconColor="#1473E6">

We're moving to the Remove Background V2 API because it delivers:

* *Cleaner cutouts* - The improved post-processing reduces matting and creates sharper edges.  
* *Higher quality automation* - Outputs with V2 are optimized for production pipelines and automated workflows.  
* *Ongoing support* - V2 is the actively supported service that will receive updates and improvements.

</AccordionItem>

<AccordionItem header="When Is This Happening?" isChevronIcon position="right" iconColor="#1473E6">

Deprecation Notice: September 2, 2025.  
End of Life (EOL): October 15, 2025.

</AccordionItem>

<AccordionItem header="Where Can I Find Resources?" isChevronIcon position="right" iconColor="#1473E6">

The latest comprehensive [information about all Photoshop APIs is available on the API Reference page](https://developer.adobe.com/firefly-services/docs/photoshop/api/#operation/removeBackground).  

For technical details specifically about the Remove Background V2 API, refer to the [Remove Background V2 endpoint](https://image.adobe.io/v2/remove-background).

</AccordionItem>

<AccordionItem header="Who Can Help Me With Migration?" isChevronIcon position="right" iconColor="#1473E6">

Your Adobe Customer Success Manager and Support Team are available to answer questions and guide you through the transition.

</AccordionItem>

</Accordion>
