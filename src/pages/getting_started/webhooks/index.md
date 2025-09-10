---
title: Using Webhooks and Events with Photoshop API
description: Learn more about the webhooks and events with the Photoshop API to help you build your applications.
hideBreadcrumbNav: true
keywords:
  - webhooks
  - events
  - Adobe I/O Events
  - Photoshop API events
  - Imaging API events
contributors:
  - https://github.com/AEAbreu-hub
---

# Understanding Photoshop API webhooks through Adobe I/O Events

## Overview

Adobe I/O Events lets you build an event-driven application based on events originating from Photoshop.
To start listening for events, your application needs to register a webhook URL, specifying the event types it expects to receive.
When a matching event gets triggered, your application is notified through an HTTP POST request to the webhook URL.

Event types represent events triggered by the individual APIs. The event provider has two event types:

* `Photoshop API events`
* `Imaging API Events`

## Registering your application and webhook

For an understanding of Adobe I/O Events:

1. See Adobe's I/O Events documentation to [create a webhook application and register your first webhook][1]
2. Explore the [sample Node.js application here][2].
3. You'll need a project on the Adobe I/O Console. Follow the steps in the [Getting Started][3] guide.

After the webhook is successfully registered, you'll start receiving events for any submitted job that either succeeded or failed,
from the event types you selected, so your application wont' need to poll for the status of the job using the job ID.

Next, see [the guide on triggering an event from the APIs][4] to learn how to put this concept into practice.

<!-- Links -->
[1]: https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md
[2]: https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/webhook-sample-app
[3]: /getting_started/index.md
[4]: /guides/triggering_an_event/index.md
