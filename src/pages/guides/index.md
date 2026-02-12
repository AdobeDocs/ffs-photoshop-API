---
title: Using these guides
description: Learn how to set up your environment and get started with the Photoshop API guides and code samples
hideBreadcrumbNav: true
keywords:
  - photoshop api
  - code samples
  - getting started
  - authentication
  - storage setup
---

# Using these guides

Review this page to get oriented before starting with the API guides. You'll learn about prerequisites, code samples, and how to set up your environment for working with the Photoshop API.

## Overview

The code snippets and example implementations throughout these guides are using one of our [sample PSD](https://github.com/AdobeDocs/cis-photoshop-api-docs/blob/main/sample_files/Example.psd) files. Feel free to download and use it for testing.

You'll need to have this file stored in accepted external storage. For more information on storage options, refer to the [File Storage](../getting_started/storage_solutions/index.md) documentation.

## Before you start

For each of these examples to run, you first need to get your Bearer token and API key. You'll find these in the [Getting Started](../getting_started/index.md) section.

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