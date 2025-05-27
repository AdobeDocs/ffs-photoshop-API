---
title: Storage Solutions
description: This page explains the storage solutions that are acceptable for use with video services.
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
---

## Rate Limits

**Hard Limit**  

- POST: 16 requests / 3 secs or 320 RPM  
- GET: 310 requests / 3 secs  

**Soft Limit**  

- POST: 15 requests / 3 secs or 300 RPM  
- GET: 300 requests / 3 secs  

#### Remove Background

**Hard Limit**  

- POST: 6 requests / 3 secs  
- GET: 1000 requests / 3 secs  

**Soft Limit**  

- POST: 2 requests / 3 secs  
- GET: 500 requests / 3 secs  

## Current limitations

There are a few limitations to the APIs you should be aware of ahead of time:

- Multi-part uploads and downloads are not yet supported.
- All the endpoints only support a single file input.
- Error handling is a work in progress. Sometimes you may not see the most helpful of messages.

## Retries

For increased reliability and stability we have added a retry mechanism for all API calls, and have some recommendations on how to handle these:

- The service will retry status codes of 429, 502, 503, 504 three times.
- You should only retry requests that have a 5xx response code. A 5xx error response indicates there was a problem processing the request on the server.
- You should implement an exponential back-off retry strategy with 3 retry attempts.
- You should not retry requests for any other response code.

## Compatibility with Photoshop versions

- The APIs will open any PSD created with Photoshop 1.0 or later.
- When saving as PSD, the APIs will create PSDs compatible with the current shipping Photoshop.
- In regards to "maximize compatibility" referenced in https://helpx.adobe.com/photoshop/using/file-formats.html#maximize_compatibility_for_psd_and_psb_files  the API's default to "yes"

## Customized workflow

You can make a customized workflow by chaining different endpoints together. [Here](/guides/code_sample/index.md#generate-remove-background-result-as-photoshop-path) is an example using the Remove Background endpoint.

## Webhooks through Adobe I/O events

Adobe I/O Events offers the possibility to build an event-driven application, based on events originating from Photoshop. To start listening for events, your application needs to register a webhook URL, specifying the Event Types to receive. Whenever a matching event gets triggered, your application is notified through an HTTP POST request to the webhook URL.
The Event Provider for the Photoshop API is `Imaging API Events`.
This event provider has two event types:

1. `Photoshop API events`

As the names indicate, these event types represent events triggered by the individual APIs.

### Registering your application to our Event Provider

#### Prerequisites needed to use the Event Provider

1. In order to use the Adobe I/O Events you will need to create a project on Adobe I/O Console.
2. You can follow the steps listed in [Getting Started](../../guides/get-started.md) page if you haven't created one yet.
3. Create a [Webhook application](https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md)

You can find a sample NodeJS application [here](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/webhook-sample-app).

#### Registering the Webhook

Once the above prerequisites are met, you can now proceed to register the webhook to the service integration. The steps to do that can be found  [here](https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md#your-first-webhook).
After the webhook has been successfully registered, you will start to receive the events for any submitted job that either succeeded or failed, from the Event Types selected. This eliminates the need for your application to poll for the status of the job using the jobID. Examples can be found [here](/guides/code_sample/index.md#triggering-an-event-from-the-apis)
