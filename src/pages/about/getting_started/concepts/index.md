---
title: Adobe Photoshop API Key Concepts
description: Learn about masks, selections and target layers
keywords:
  - Photoshop API 
  - masks
  - selections
  - layers
contributors:
  - https://github.com/archyposada
  - https://github.com/AEAbreu-hub
hideBreadcrumbNav: true
---

# Photoshop API Key Concepts

Learn these essential concepts from the Photoshop app that apply to key features of the Photoshop API.

## Overview

Some important concepts from the Photoshop app also apply when you use the Photoshop API to create and enhance images. Review the ideas on this page if you're a new user or if you want to understand the Photoshop API more thoroughly.

## About layers and the target layer

In the Photoshop app, **layers** are used to stack different parts of an image. Layers are like transparent panes of glass stacked on top of each other, allowing you to work with different elements of an image independently. You can paint on each layer, add photos, or add vector without affecting the content on other layers. You can view each layer in the Layers Panel in the Photoshop app.

Let's look at an example image to understand this idea. Here's an image with three layers:

![alt image](./all_layers.png?raw=true "Original Image")

Separating the image into its layers looks like this:

![alt image](./decompose_layers.png?raw=true "Original Image")

Choosing to view just one layer, such as the earth in the image, looks like this:

![alt image](./layers_earth.png?raw=true "Original Image")

In both the Photoshop app and the API, there is the concept of the **target layer**. This is the selected layer and any operations you perform *only apply to this layer*.

For example, using the astronaut as the target layer and resizing it only applies to that layer, and this is the result:

![alt image](./astronaut_resize.png?raw=true "Original Image")

Layers that you define in the Photoshop app organize an image into manageable parts. Then with the Photoshop API, make isolated image adjustments by applying changes only to a target layer.

For more information about layers, see [Photoshop, layer basics](https://helpx.adobe.com/photoshop/using/layer-basics.html).

## About selections

In the Photoshop app, a **selection** defines an area in an image that we want to enhance or adjust. Just as with target layers, any operation you perform only applies to the selection itself.

![alt image](./astronaut_selection.png?raw=true "Original Image")

For example, in the image above the pink area is the selection made with the Photoshop app. Now the Photoshop API can make adjustments (like inserting a new background or expanding the selection) to that specific area.

To learn more, see [Photoshop, Getting started with selections](https://helpx.adobe.com/photoshop/using/making-selections.html).

## About masks

In the Photoshop app, **masks** selectively control the visibility of a layer's content without permanently deleting or altering that content. They determine which parts of a layer are shown or hidden, offering more editing flexibility than deleting pixels.

You can define a mask in your Photoshop app and later manipulate that part of the image with Photoshop API. Masking is a great way to:

- Make image composites.
- Modify background colors.
- Remove or cut out objects.
- Target image adjustments so they affect only certain areas rather than the entire layer.

For example, this image has two layers, with the earth and space in the background and the moon in the foreground:

![alt image](./mask_background.png?raw=true "Original Image")

On the moon layer, we can define an area to mask out:

![alt image](./mask_outline.png?raw=true "Original Image")

After applying the mask, the earth and space background from the bottom layer shows through the area that was masked:

![alt image](./mask_applied.png?raw=true "Original Image")

Unlike selections and layers, enhancements apply to the mask itself, not the image being masked, and sophisticated image adjustments can be made without deleting or permanently altering source images.

To learn more about masks in Photoshop, see [Photoshop, Mask Layers](https://helpx.adobe.com/photoshop/using/masking-layers.html).
