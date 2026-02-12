---
title: Enhance quality with Refine Mask
description: Learn how to use the Refine Masks API to enhance image mask quality.
hideBreadcrumbNav: true
keywords:
  - refine mask
  - image processing
  - mask refinement
  - photoshop api
---

# Enhance image mask quality with Refine Mask

Learn how to use the Refine Masks API in your code workflows with this guide to enhance image mask quality.

## Overview

In this tutorial, you'll learn how to use the Mask Refinement API to enhance the quality of your image masks. Whether you're working on image segmentation, graphic design, or any project that requires precise mask details, our API will help you achieve cleaner, smoother edges and more accurate mask representations.

Follow along to see how easy it is to integrate this powerful tool into your workflow and elevate your image-processing tasks.

## About the Refine Masks API

Before getting into the code, let's consider how the Refine Masks API works at a high level.

- You begin with a source image, uploaded to one of the supported cloud storage providers. See the API reference for the list of supported cloud storage providers.
- You then provide a *masked* version of the image. The Photoshop API will refine the mask according to the source image.
- You can provide a single mask for the input image that needs to be refined.

<InlineAlert variant="help" slots="text" />

Use the [v1/mask-objects](../../api/index.md) endpoint first to generate masks to provide in your requests to this endpoint.

## Prerequisites

-  Valid credentials. If you don't have them yet, first visit the Firefly Services [Getting Started](../index.md) guide to obtain a `client_id` and `client_secret`.
-  Node.js installed on your machine and basic familiarity with `JavaScript`.
-  Store the source and mask images below in a supported cloud storage provider.

### Source image

![Source image](../../assets/source-image-refinement.jpg)

### Mask image

![Mask image](../../assets/mask-image-refinement.png)

## Using color decontamination

The `colorDecontamination` parameter determines whether color decontamination should be applied to the foreground of the input image. When set to `true`, the API will remove any color fringing and contamination from the foreground, ensuring a more accurate and clean RGBA mask output.

## Calling the Refine Masks API

Here is a simple example of the request body required to use the Refine Masks API:

```json
{
  "image": {
    "source": {
      "url": "<source_image_url>"
    }
  },
  "mask": {
    "source": {
      "url": "<mask_image_url>"
    }
  },
  "colorDecontamination": false
}
```

The source of the images, take pre-signed URLs from the cloud storage provider.

## Generated result

You can see in the image below that the mask has been refined.

**Result without color decontamination**

![Generated Result](../../assets/result-image-refinement.png)

**Result with color decontamination**

![Color Decontaminated Result](../../assets/result-image1-color.png)

## Complete sample code

If it's helpful to see a complete implementation, we've provide the full JavaScript code sample.

<Accordion>

<AccordionItem header="Full code sample" isChevronIcon  position="right" iconColor="#1473E6">

```js
const axios = require("axios");
 
// REST API's status codes
const STATUS_ACCEPTED = 202;
const DEFAULT_SERVICE_BASE_URL = "https://api-facade-service-stage.adobe.io";
 
// object containing api endpoints
const apiEndpoints = {
  REFINE_MASK: "/v1/refine-mask",
};
 
/**
 * Function to make get api call
 * @param {string} url - Api end point
 * @param {object} headers - headers to be passed
 * @returns {Promise} - Response of the API call
 */
function makeGetCall(url, headers) {
  return axios.get(url, { headers });
}
 
/**
 * Function to make post api call
 * @param {string} url - Api end point
 * @param {object} payload - Payload to be passed
 * @param {object} headers - Headers to be passed
 * @returns {Promise} - Response of the API call
 */
function makePostCall(url, payload, headers) {
  return axios.post(url, payload, { headers });
}
 
/**
 * Function to make service api calls
 *  - post api call to get the status url
 *  - get api call to get the result
 * @param {string} url - Api end point
 * @param {object} payload - Payload to be passed
 * @param {object} headers - Headers to be passed
 * @returns {Promise} - Object of image urls and its properties
 */
async function makeServiceApiCall(url, payload, headers) {
  const postResponse = await makePostCall(url, payload, headers);
  if (postResponse.status === STATUS_ACCEPTED) {
    const statusUrl = postResponse.data.statusUrl;
    const getResult = await makeGetCall(statusUrl, headers);
    return getResult.data;
  } else {
    console.log("Error in serviceApiCall post operation ", postResponse);
  }
}
 
/**
 * Function to refine mask of the image
 * @param {object} payload - payload with image and masks
 * @param {object} headers - headers to be passed
 * @returns {Promise} - object containing foreground object images
 */
async function refineMask(headers, serviceBaseUrl, payload) {
  try {
    const endpoint = new URL(
      apiEndpoints.REFINE_MASK,
      serviceBaseUrl
    ).toString();
    return makeServiceApiCall(endpoint, payload, headers);
  } catch (error) {
    console.log("Error inside refineMask function ", error);
  }
}
 
/**
 * Function to fetch token
 * @returns {Promise} - token string
 */
async function fetchAccessToken() {
  //TODO: Implement logic to fetch token
  const token = "Bearer <your_access_token>";
  return token;
}
 
/**
 * Function to generate headers
 * @returns {Promise} - headers object
 */
async function generateHeaders() {
  // const apiKey = await fetchApiKey();
  const token = await fetchAccessToken();
  const headers = {
    "Content-Type": "application/json",
    // Update X-Api-Key with the actual api key
    "X-Api-Key": "<your_api_key>",
    Authorization: token,
  };
  return headers;
}
 
async function main() {
  // update serviceBaseUrl
  const serviceBaseUrl = "<your_service_base_url>" || DEFAULT_SERVICE_BASE_URL;
  // update sourceImageUrl with the source image url
  const sourceImageUrl = "<your_source_image_url>";
  // update maskUrl with the mask url
  const maskUrl = "<your_mask_url>";
  const headers = await generateHeaders();
 
  const payload = {
    image: {
      source: {
        url: sourceImageUrl
      }
    },
    mask: {
      source: {
        url: maskUrl
      }
    },
    colorDecontamination: false
  };
  const result = await refineMask(headers, serviceBaseUrl, payload);
  return result;
}
 
main();
```

</AccordionItem>

</Accordion>
