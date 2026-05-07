---
title: Photoshop API Overview
description: This is the overview page of Adobe Photoshop API
keywords:
  - Photoshop API guides
  - Photoshop API Overview
  - Photoshop API documentation
  - Photoshop API
  - Photoshop API SDK
  - Photoshop API Developer documentation
  - Photoshop API v2
  - Photoshop v2 API
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
---

<Superhero slots="image, heading, text"/>

![Hero image](./assets/hero.png)

# Adobe Photoshop API - Firefly Services

Unlock the potential of Adobe Photoshop and cutting edge AI/ML services through an easy-to-use RESTful API.

<Announcement slots="heading, text, button" variant="secondary" backgroundColor="background-color-gray" borderColor="#14b8a6" hasborder="true"/>

#### 🚀 Now Generally Available - Photoshop API v2 

Photoshop API v2 is now generally available. This release introduces major improvements in scalability, flexibility, and programmability, enabling teams to build production-grade, high-volume content workflows. v2 addresses these gaps and introduces a more extensible foundation for modern content pipelines.

- [Learn more](/getting-started/v2-ga/index.md)

## Overview

Welcome to the Adobe Photoshop API, now integrated into Firefly Services. Our API follows REST-like principles, utilizing standard HTTP response codes, verbs, and authentication methods that return JSON-encoded responses. While the examples provided are in cURL, feel free to develop your application in any preferred language.

This guide will assist you in:

- Creating a project within the Adobe Developer Console
- Obtaining and authenticating your credentials
- Constructing personalized workflows by chaining API calls to various endpoints within the Firefly Services APIs
- Developing event-driven applications through Adobe I/O Events

## What Photoshop API services are available?

Many useful Photoshop operations are available as services with the Photoshop API. Explore how to integrate and use the available Photoshop API services in the [Photoshop API guides](/guides/index.md).

Here are just a few of the available services:

* **[Remove background](/guides/remove-background/index.md)** — Detect and isolate the main subject with AI and remove the background while preserving the subject for use in composites and cutouts.
* **[Smart Objects](/guides/smart-objects-and-the-api/index.md)** — Create and replace embedded Smart Objects in a PSD so new imagery fits the original layer bounds and keeps its aspect ratio.
* **[Product Crop](/guides/product-crop/index.md)** — Smart-crop images by detecting the subject and framing it as the focal point (single-layer inputs; multilayer PSDs are not supported).
* **[ActionJSON](/guides/actionjson-endpoint/index.md)** — Apply Photoshop Actions from an ATN file programmatically and adjust the action payload for more flexible, dynamic edits than a static action alone.

You can also review the endpoints in [the latest and greatest Photoshop v2 API](#what-is-photoshop-api-v2) or the legacy Photoshop v1 API in the reference documentation:

- [Photoshop API v1](/api/index.md)
- [Photoshop API v2](/api/photoshop-v2/index.md)

## What is Photoshop API v2?

The **Photoshop API v2** is a unified next-generation surface for Photoshop and Lightroom-style workflows in Firefly Services: one architecture, consistent request and response patterns, and flexible output destinations. Use it when you want combined operations in fewer round trips, clearer status handling, and migration paths from the legacy v1 Photoshop and Lightroom APIs.

### What improvements does Photoshop API v2 offer?

Photoshop API v2 allows you to:

* **Run Photoshop operations** — Create composites, edit documents and layers, execute actions, generate manifests, and create artboards through versioned `/v2` endpoints.
* **Check asynchronous jobs** — Poll job status with a dedicated job-status model aligned to the v2 pipeline.
* **Integrate storage flexibly** — Use embedded, hosted, and external storage patterns with clear destination configuration.
* **Regenerate storage URLs when needed** — Use storage-related endpoints where applicable for your deployment.

### What new features does Photoshop API v2 offer?

- **Combined operations** – Apply multiple edits in a single request instead of multiple API calls.
- **Flexible storage options** – Embedded, hosted, presigned, and Creative Cloud storage.
- **Published action files** – Inspect and customize the action definitions behind convenience workflows.
- **Enhanced layer operations** – Richer layer control via the create-composite endpoint.
- **Improved error handling** – Clearer error codes, multiple validation details, and a consistent error shape.

### How can I use the Photoshop API v2?

Explore the Photoshop API v2 migration guides to learn how to change existing implementations to use the improved v2 API.

* **[Photoshop API v2 migration guides](/guides/photoshop-v2/index.md)** — Migration overviews, v1-to-v2 topics, and workflow guides for the v2 API.
* **[Photoshop API v2 reference](/api/photoshop-v2/index.md)** — Full endpoint reference for the `photoshopv2-api.json` specification.

## Discover

<DiscoverBlock slots="heading, link, text"/>

### Get Started

[Getting Started Guide](/getting-started/index.md)

Get started with the Adobe Photoshop Firefly Services.

<DiscoverBlock slots="link, text"/>

[Tutorials](/guides/index.md)

Explore our tutorials page for comprehensive guidance.  

<DiscoverBlock slots="link, text"/>

[API Reference](/api/index.md)

See the API reference page for detailed technical information about the API.

<DiscoverBlock slots="link, text"/>

[Photoshop API v2 guides](/guides/photoshop-v2/index.md)

Review migration guides and other Photoshop API v2 topics. For authentication and storage, use the [Getting Started](/getting-started/index.md) section.

<DiscoverBlock slots="link, text"/>

[Photoshop API v2 reference](/api/photoshop-v2/index.md)

Browse the OpenAPI reference for Photoshop API v2 endpoints.
