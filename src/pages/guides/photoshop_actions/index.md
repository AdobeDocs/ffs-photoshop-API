---
title: Photoshop Actions
description: Photoshop Actions documentation
---

# Photoshop Actions

*Actions* are a series an image adjustment that you can record in the Photoshop app and then you can later apply to one or more images.

Typically, you apply actions on a single file or a batch of files and you record actions from Photoshop app menu commands, panel options, tool actions, and more.

![alt image](frogs_adjusted.png?raw=true "Original Image")

For example, you can create an action file that changes the hue and saturation of an image, applies a slight blur effect to the image, and then saves the file in the desired format. In the Photoshop app, you create a sequence of actions and then save these image adjustments in a single file, known as an ATN file. You can later call the Photoshop API to run one or more actions from your ATN file and apply these actions to multiple images.

For background information on Photoshop Actions, see the <a href="https://helpx.adobe.com/photoshop/using/actions-actions-panel.html" target="_blank">Adobe Help Center.</a>

### Supported Input and Output formats

We support the following file formats for Photoshop API with Photoshop Actions:

* PSD
* JPEG
* PNG
* TIFF

### Best Practices and Limitations

* We support all Photoshop app dialogs, however we do not support interactions with operating system dialogs. The later means you cannot use Photoshop API to programmatically open a system-level print settings dialog.
* We recommended creating Actions that do not require user intervention such as confirming a selection or providing file paths.
* Make sure to test your actions on Photoshop, with several different input/images. If it has any errors in Photoshop, it won't run successfully on our servers either.

The following are known limitations which Photoshop API does not support:

* Photoshop 3D, and Video and animation features features.
* Custom presets, for example color swatches and brushes.
* This endpoint does not currently support multiple file inputs.

You can choose to playback all of the tasks recorded in an Action or you can selectively choose a particular task from an Actions file and exclude the rest.

### Examples

In this example we applied a custom Action called Posterize. This ATN file had multiple recorded Photoshop tasks including Select Subject, Remove Background, Posterize, and Export as PNG.

![alt image](spaniels_before_after.png?raw=true "Original Image")

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/photoshopActions \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "https://as2.ftcdn.net/jpg/02/49/48/49/500_F_249484911_JifPIzjUqzkRhcdMkF9GnsUI9zaqdAsn.jpg",
      "storage": "external"
    }
  ],
  "options": {
    "actions": [
      {
        "href": "https://raw.githubusercontent.com/johnleetran/ps-actions-samples/master/actions/Posterize.atn",
        "storage": "external"
      }
    ]
  },
  "outputs": [
    {
      "storage": "<storage>",
      "type": "image/jpeg",
      "href": "https://some-presigned-url/output.jpeg"
    }
  ]
}'
```

For another example, see [Execute Individual Photoshop Action](../../guides/code_sample/index.md#photoshop-actions-play-a-specific-action) 

### Photoshop Actions Play a specific action

By default, Photoshop API will attempt to play all actions in an action set.  If you would like to only playback a specific action, you can specify `actionName` and the name of the action you want to invoke (see example below).

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/photoshopActions \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "https://as2.ftcdn.net/jpg/02/49/48/49/500_F_249484911_JifPIzjUqzkRhcdMkF9GnsUI9zaqdAsn.jpg",
      "storage": "external"
    }
  ],
  "options": {
    "actions": [
      {
        "href": "https://raw.githubusercontent.com/johnleetran/ps-actions-samples/master/actions/Oil-paint.atn",
        "storage": "external",
        "actionName": "Action 51"
      }
    ]
  },
  "outputs": [
    {
      "storage": "<storage>",
      "type": "image/jpeg",
      "href": "https://some-presigned-url/output.jpeg"
    }
  ]
}'
```