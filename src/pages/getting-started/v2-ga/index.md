---
title: Photoshop API v2 — General Availability
description: Photoshop API v2 is now generally available with scalability, flexibility, and programmability improvements for production workflows.
hideBreadcrumbNav: true
keywords:
  - photoshop api v2
  - general availability
  - ga
  - migration
  - linked smart objects
contributors:
  - https://github.com/AEAbreu-hub
---

# Photoshop API v2 — General Availability

Photoshop API v2 is now generally available. This release introduces major improvements in scalability, flexibility, and programmability, enabling teams to build production-grade, high-volume content workflows.

If you've worked with v1, you likely encountered limitations around file size, embedded assets, and rigid workflows. v2 addresses these gaps and introduces a more extensible foundation for modern content pipelines.

## What's New

### Linked Smart Objects

Photoshop API v2 adds support for linked smart objects, a foundational improvement for content supply chains.

In v1, embedded smart objects created several challenges:

* PSD files increased in size quickly and often exceeded the 2GB limit.
* Assets were duplicated across files instead of reused.
* Updating assets downstream was difficult to manage and govern.

With linked smart objects:

* Assets are referenced instead of embedded.
* File sizes remain manageable, even in large-scale workflows.
* Updates propagate across templates and variants.
* Teams can centralize and govern shared assets.

This enables more efficient, maintainable, and scalable content systems.

### Increased File Size Limits

Maximum file size increased from 2GB to 5GB.

This allows for significantly more complex documents and removes a key limitation for enterprise use cases.

### UXP Scripting (JavaScript Automation)

Photoshop API v2 introduces support for UXP scripting, allowing developers to execute JavaScript directly within Photoshop workflows.

This adds a programmable layer to automation and unlocks advanced use cases:

* Copy fitting and dynamic text adjustments.
* Conditional logic based on inputs or metadata.
* Automated recoloring and localization.
* Trapping and print-specific adjustments.
* Compliance and brand rule enforcement.

Previously, these scenarios required custom workarounds or waiting for new API capabilities.

With UXP scripting:

* Teams can define and maintain their own logic.
* Business rules can be embedded directly into workflows.
* Automation becomes extensible rather than fixed.

This significantly expands what can be built with the API.

### More Powerful Action Workflows

* Support for Generative Fill, Generative Expand, and additional actions.
* Adobe action files are now published and customizable.
* Outputs can be dynamically generated at runtime without predefining assets.

### Richer Document Intelligence

* Artboards are now first-class objects with full metadata (size, presets, background).
* Ability to extract embedded smart objects without opening Photoshop.
* Expanded layer metadata including text settings, blend ranges, and layout details.

### Expanded Creative Control

* Improved smart object workflows with support for SVG and linked assets.
* New replacement and transformation capabilities.
* Enhanced text rendering for complex and multilingual content.
* Improved color management with ICC profile support.

### Built for Scale

* Support for files up to 5GB.
* Longer processing times for complex jobs.
* Improved error handling with more actionable responses.
* Flexible storage options for both prototyping and production workflows.

## Migration Notice

Photoshop API v1 will reach end of life on **July 31, 2026**.

Teams should begin planning migration to v2 to take advantage of the new capabilities and avoid disruption.

## Documentation

[Photoshop API v2 reference](/api/photoshop-v2/index.md)
