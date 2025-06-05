---
title: Technical usage notes
description: Learn about current limitations, rate limits, and best practices for implementing the Photoshop API.
hideBreadcrumbNav: true
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
  - https://github.com/AEAbreu-hub
keywords:
  - limitations
  - rate limits
  - retries
  - compatibility
  - webhooks
  - events
---

# Technical Usage Notes

This document has details about what's currently supported, limitations, and workarounds for the Photoshop API to help optimize your API implementations and understand service boundaries.

## Known limitations

These are known limitations to the APIs to be aware of:

- Multi-part uploads and downloads aren't yet supported.
- All endpoints only support a single file input.
- Error handling is a work in progress - you may not always see the most helpful error messages.

## Retries

For increased reliability and stability, there's a retry mechanism for all API calls:

- The service will retry status codes of 429, 502, 503, 504 three times.
- You should only retry requests that have a 5xx response code - this indicates there was a problem processing the request on the server.
- You should implement an exponential back-off retry strategy with 3 retry attempts.
- You shouldn't retry requests for any other response code.

## Compatibility with Photoshop versions

- The APIs will open any PSD created with Photoshop 1.0 or later.
- When saving as PSD, the APIs will create PSDs compatible with the current shipping Photoshop.
- Regarding "maximize compatibility" referenced in the [Photoshop file formats documentation][1], the APIs default to "yes".

## Rate limits

**Hard limit**

- POST: 16 requests / 3 secs or 320 RPM.
- GET: 310 requests / 3 secs.

**Soft limit**

- POST: 15 requests / 3 secs or 300 RPM.
- GET: 300 requests / 3 secs.

### Remove background

**Hard limit**

- POST: 6 requests / 3 secs.
- GET: 1000 requests / 3 secs.

**Soft limit**

- POST: 2 requests / 3 secs.
- GET: 500 requests / 3 secs.

## Customized workflow

You can make a customized workflow by chaining different endpoints together. See an [example of using the Remove Background endpoint][2].

## Webhooks through Adobe I/O Events

Adobe I/O Events lets you build an event-driven application based on events originating from Photoshop. To start listening for events, your application needs to register a webhook URL, specifying the event types to receive. When a matching event gets triggered, your application is notified through an HTTP POST request to the webhook URL.

The event provider for the Photoshop API is `Imaging API Events`. This event provider has two event types:

1. `Photoshop API events`

As the names indicate, these event types represent events triggered by the individual APIs.

### Registering your application to our event provider

#### Prerequisites needed to use the event provider

1. You'll need to create a project on the Adobe I/O Console to use Adobe I/O Events
2. Follow the steps listed in the [Getting Started][3] page if you haven't created one yet
3. Create a [webhook application][4]

You can find a sample Node.js application [here][5].

#### Registering the webhook

Once you've met the above prerequisites, you can proceed to register the webhook to the service integration. Follow the steps [here][4] to register your first webhook.

After the webhook has been successfully registered, you'll start receiving events for any submitted job that either succeeded or failed, from the event types you selected. This eliminates the need for your application to poll for the status of the job using the job ID. See examples [here][6].

<!-- Links -->
[1]: https://helpx.adobe.com/photoshop/using/file-formats.html#maximize_compatibility_for_psd_and_psb_files
[2]: /guides/code_sample/index.md#generate-remove-background-result-as-photoshop-path
[3]: /getting_started/index.md
[4]: https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md
[5]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/webhook-sample-app
[6]: /guides/code_sample/index.md#triggering-an-event-from-the-apis
