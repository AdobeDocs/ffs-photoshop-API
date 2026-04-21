---
title: Photoshop API v1 Guides
description: Learn how to set up your environment and get started with the Photoshop API v1 guides and code samples
hideBreadcrumbNav: true
keywords:
  - photoshop api v1
  - code samples
  - getting started
  - authentication
  - storage setup
---

# Photoshop API v1 guides

Review this page to get oriented before starting with the API guides. You'll learn about prerequisites, code samples, and how to set up your environment for working with the Photoshop API v1.

## Overview

The code snippets and example implementations throughout these guides are using one of our [sample PSD](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.psd) files. Feel free to download and use it for testing.

You'll need to have this file stored in accepted external storage. For more information on storage options, refer to the [File Storage](../getting-started/storage-solutions/index.md) documentation.

## Before you start

For each of these examples to run, you first need to get your Bearer token and API key. You'll find these in the [Getting Started](../getting-started/index.md) section.

For ease of use, you can export your token and API key before running the examples:

```shell
export token="<your_token>"
```

```shell
export apiKey="<your_api_key>"
```

## Working with code samples

Code samples in these guides include:

- Complete cURL commands with proper headers
- Example request payloads
- Expected response formats

Make sure to replace placeholder values with your actual credentials and file URLs before running any examples.

## Migrating from v1?

<Edition slots="text" backgroundcolor='blue' />

beta

If you're already using the legacy Photoshop or Lightroom APIs (v1), the Photoshop v2 beta API offers a unified architecture, combined operations in a single call, and more flexible storage—with a clear path to migrate.

**Start here:**

* **[Migration to v2 overview](photoshop-v2-beta/v1-to-v2/index.md)** — What's changing, breaking changes, and a step-by-step migration path with a reference table that maps each v1 endpoint to its v2 equivalent and the right guide.
* **[Key improvements and architecture with v2](photoshop-v2-beta/v1-to-v2/key-improvements.md)** — Why migrate: combined operations, flexible storage options, published action files, and other architectural benefits.

From the migration overview you can jump to detailed guides for your endpoints: edit operations, format conversion, document creation, layer operations, actions, artboards, manifest, status, and convenience APIs.
