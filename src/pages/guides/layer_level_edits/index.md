---
title: Layer level edits
description: Layer level edits documentation
---

# Layer level edits

* General layer edits
  * Edit the layer name.
  * Toggle the layer locked state.
  * Toggle layer visibility.
  * Move or resize the layer via it's bounds.
  * Delete layers.
* Adjustment layers
  * Add or edit an adjustment layer. The following types of adjustment layers are currently supported:
    * Brightness and Contrast.
    * Exposure.
    * Hue and Saturation.
    * Color Balance.
* Image/Pixel layers
  * Add a new pixel layer, with optional image.
  * Swap the image in an existing pixel layer.
* Shape layers
  * Resize a shape layer via it's bounds.

### Add, edit and delete layers

The `/documentOperations` API should primarily be used to make layer and/or document level edits to your PSD and then generate new renditions with the changes. You can pass in a flat array of only the layers that you wish to act upon, in the `options.layers` argument of the request body.
The layer name (or the layer id) will be used by the service to identify the correct layer to operation upon in your PSD.

The `add`, `edit`, `move` and `delete` blocks indicate the action you would like to be taken on a particular layer object. Any layer block passed into the API that is missing one of these attributes will be ignored.
The `add` and `move` blocks must also supply one of the attributes `insertAbove`, `insertBelow`, `insertInto`, `insertTop` or `insertBottom` to indicate where you want to move the layer to. More details on this can be found in the API reference.

**Note**: Adding a new layer does not require the ID to be included, the service will generate a new layer id for you.

Here are some examples of making various layer level edits.

* [Layer level editing](/guides/code_sample/index.md#making-a-simple-edit)
* [Adding a new Adjustment Layer](/guides/code_sample/index.md#adding-a-new-adjustment-layer)
* [Editing Image in a Pixel Layer](/guides/code_sample/index.md#editing-a-pixel-layer) 