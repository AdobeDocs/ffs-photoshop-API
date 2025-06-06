---
title: Webhooks
description: Learn how to use webhooks to receive events from the Photoshop API.
hideBreadcrumbNav: true
---

# Webhooks through Adobe I/O Events\

## Overview

Adobe I/O Events lets you build an event-driven application based on events originating from Photoshop.
To start listening for events, your application needs to register a webhook URL, specifying the event types to receive.
When a matching event gets triggered, your application is notified through an HTTP POST request to the webhook URL.

Event types represent events triggered by the individual APIs. The event provider has two event types:

1. `Photoshop API events`
2. `Imaging API Events`

### Registering your application to our event provider

#### Prerequisites needed to use the event provider

1. You'll need to create a project on the Adobe I/O Console to use Adobe I/O Events
2. Follow the steps listed in the [Getting Started][3] page if you haven't created one yet
3. Create a [webhook application][4]

You can find a sample Node.js application [here][5].

#### Registering the webhook

Once you've met the above prerequisites, you can proceed to register the webhook to the service integration.
Follow the steps [here][4] to register your first webhook.

After the webhook has been successfully registered, you'll start receiving events for any submitted job that either succeeded or failed,
from the event types you selected.
This eliminates the need for your application to poll for the status of the job using the job ID. See examples [here][6].

<!-- Links -->
[3]: /getting_started/index.md
[4]: https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md
[5]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/webhook-sample-app
[6]: /guides/code_sample/index.md#triggering-an-event-from-the-apis
