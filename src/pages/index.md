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
  - Photoshop v2 beta
  - Photoshop v2 API
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
---

<Superhero slots="image, heading, text"/>

![Hero image](./assets/hero.png)

# Adobe Photoshop API - Firefly Services

Unlock the potential of Adobe Photoshop and cutting edge AI/ML services through an easy-to-use RESTful API.

## Overview

Welcome to the Adobe Photoshop API, now integrated into Firefly Services. Our API follows REST-like principles, utilizing standard HTTP response codes, verbs, and authentication methods that return JSON-encoded responses. While the examples provided are in cURL, feel free to develop your application in any preferred language.

This guide will assist you in:

- Creating a project within the Adobe Developer Console
- Obtaining and authenticating your credentials
- Constructing personalized workflows by chaining API calls to various endpoints within the Firefly Services APIs
- Developing event-driven applications through Adobe I/O Events

## Photoshop v2 beta

The **Photoshop v2 beta** API is a unified next-generation surface for Photoshop and Lightroom-style workflows in Firefly Services: one architecture, consistent request and response patterns, and flexible output destinations. Use it when you want combined operations in fewer round trips, clearer status handling, and migration paths from the legacy v1 Photoshop and Lightroom APIs.

### What is Photoshop v2 beta?

Photoshop v2 beta allows you to:

* **Run Photoshop operations** — Create composites, edit documents and layers, execute actions, generate manifests, and create artboards through versioned `/v2` endpoints.
* **Check asynchronous jobs** — Poll job status with a dedicated job-status model aligned to the v2 pipeline.
* **Integrate storage flexibly** — Use embedded, hosted, and external storage patterns with clear destination configuration.
* **Regenerate storage URLs when needed** — Use storage-related endpoints where applicable for your deployment.

### Features

* **Unified API** — Photoshop-oriented image processing plus job lifecycle and storage helpers documented under a single OpenAPI specification.
* **Clear versioning** — `v2` paths and beta reference documentation kept separate from the shipping Photoshop API reference for easier comparison and migration.
* **Guides for migrating from v1** — Topic-based migration guides for edit, document, layer, actions, output, artboard, manifest, and status flows.

### Next steps

* **[Photoshop v2 beta guides](/guides/photoshop-v2-beta/index.md)** — Migration overviews, v1-to-v2 topics, and getting started topics scoped to the v2 beta.
* **[Photoshop v2 beta API reference](/api/photoshop-v2-beta/index.md)** — Full endpoint reference for the `photoshopv2-api.json` specification.

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

[Photoshop v2 beta guides](/guides/photoshop-v2-beta/index.md)

Review migration guides and other v2 beta topics for the Photoshop v2 beta API. For authentication and storage, use the [Getting Started](/getting-started/index.md) section.

<DiscoverBlock slots="link, text"/>

[Photoshop v2 beta API reference](/api/photoshop-v2-beta/index.md)

Browse the OpenAPI reference for Photoshop v2 beta endpoints.
