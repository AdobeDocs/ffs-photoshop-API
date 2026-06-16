---
title: AutoCrop API Feature Guide
description: Learn how Firefly's AutoCrop API automatically generates aesthetically pleasing and contextually relevant crops for images and video thumbnails.
hideBreadcrumbNav: true
keywords:
  - autocrop
  - smart crop
  - automatic cropping
  - subject detection
  - priority object crop
  - super box crop
  - video thumbnails
contributors:
  - https://github.com/AEAbreu-hub
---

# AutoCrop

Perform automatic cropping on images or video thumbnails.

## What is AutoCrop API?

Firefly's AutoCrop API is a smart cropping service that automatically generates aesthetically pleasing and contextually relevant crops and resizing of images or video thumbnails. It leverages deep learning models to detect and preserve key foreground objects.

The service is designed to support these key scenarios:

### Smart crop

Given an image and a target resolution, the service returns an optimal crop.

* Automatically detects and preserves the main subject(s) of the image.
* Generates a visually balanced crop tailored to the target aspect ratio.
* Ideal for thumbnails, banners, or platform-specific aspect ratios.

### Priority object crop

Given an image, a target resolution, and a list of objects, the service returns a crop that prioritizes these objects.

* Performs object detection and reorders cropping logic based on the specified list.
* Higher-priority objects are more likely to be included in the crop.
* Best for editorial workflows or product-centric cropping.

### Full subject crop

Given an image, the service returns the minimum bounding crop that contains all detected foreground objects.

* Ignores aspect ratio constraints to generate a tight fit around all relevant content.
* Primarily used for hero shots or full-scene object framing, or as a fallback if the aspect-ratio crop isn't feasible.

### Object detection and Super Box crop

Given an image, the service returns bounding boxes for all detected objects, and a subject crop—a "Super Box" that encloses all detected objects.

* Enables downstream workflows like tagging, reflow design, and variant generation.
* The Super Box may optionally be used as a crop where context retention is more important than aspect ratio.
