---
title: Artboards
description: Artboards documentation
---

# Artboards

Artboards in the Photoshop API let you create a single document from multiple input images and read artboard data from generated manifests.

## Artboard information in the JSON Manifest

When you generate a manifest for a document that contains artboards, the response includes an `artboards` array with structure and bounds.

## Create a new artboard from multiple input images

You can create a new artboard document from multiple input images (e.g. PSDs or other supported image types) using the `/v2/create-artboard` endpoint. The API arranges the images horizontally with optional spacing.

For full request/response details, see the [API reference](../../api/photoshop-v2/index.md).
