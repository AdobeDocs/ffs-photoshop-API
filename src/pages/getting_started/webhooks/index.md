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

# Photoshop API webhooks and Adobe I/O Events

Understand Adobe I/O Events and how you can set up your application to receive events from Photoshop.

## Registering your application and webhook

Adobe I/O Events lets you build an event-driven application based on events originating from Photoshop.
To start listening for events, your application needs to register a webhook URL, specifying the event types it expects to receive.
When a matching event gets triggered, your application is notified through an HTTP POST request to the webhook URL.

Event types represent events triggered by the individual APIs. The event provider has two event types:

* `Photoshop API events`
* `Imaging API Events`

For a comprehensive understanding of Adobe I/O Events:

1. See Adobe's I/O Events documentation to [create a webhook application and register your first webhook](https://www.adobe.io/apis/experienceplatform/events/docs.html#!adobedocs/adobeio-events/master/intro/webhooks_intro.md).
2. Explore the [sample Node.js application here](https://github.com/AdobeDocs/cis-photoshop-api-docs/tree/main/sample-code/webhook-sample-app).
3. You'll need a project on the Adobe I/O Console. To create one, follow the steps in the [Getting Started](/getting_started/index.md) guide.

After the webhook is successfully registered, you'll start receiving events from the event types you selected for any submitted job that has succeeded or failed so that your application won't need to poll for the status of the job using the job ID.

Next, see [the guide on triggering an event from the APIs](/guides/triggering_an_event/index.md) to learn how to put this concept into practice.
