---
title: Artboards
description: Artboards documentation
---

# Artboards

Artboards in the Photoshop API let you create a single document from multiple input images and read artboard data from generated manifests.

## Artboard information in the JSON Manifest

When you generate a manifest for a document that contains artboards, the response includes an `artboards` array with structure and bounds. See the [Manifest Migration](../photoshop-v2-beta/v1-to-v2/manifest-migration.md) guide for the manifest structure, or the [Generate Manifest Endpoint](../retrieve-manifest/index.md) for the request flow.

## Create a new artboard from multiple input images

You can create a new artboard document from multiple input images (e.g. PSDs or other supported image types) using the `/v2/create-artboard` endpoint. The API arranges the images horizontally with optional spacing.

For full request/response details, examples, output formats, and migration from the v1 artboards endpoint, see the [Artboard Migration (V1 to V2)](../photoshop-v2-beta/v1-to-v2/artboard-migration.md) guide.
