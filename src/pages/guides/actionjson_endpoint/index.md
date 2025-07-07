---
title: Using the ActionJSON Endpoint
description: Learn how to use the ActionJSON endpoint to apply and modify Photoshop Actions programmatically with enhanced flexibility.
hideBreadcrumbNav: true
keywords:
  - actionjson
  - photoshop actions
  - ATN files
  - batch processing
  - developer mode
contributors:
  - https://github.com/AEAbreu-hub
---

# Getting started with ActionJSON

ActionJSON is similar to the Photoshop Actions endpoint, allowing you to apply the contents of an ATN file to an image programmatically. However, there is added flexibility when you use ActionJSON.

The `/actionJSON` endpoint accepts an input file, applies any Photoshop Action file to it, and edits the steps within the original action file to create dynamic changes to an otherwise static Action file.

These changes can include:

* Modifying the payload, such as adding an action.
* Applying an ATN file to an image without uploading and storing your ATN file at Firefly Services as you do with the Photoshop Actions endpoint.

Watch this tutorial video and read on to learn more about ActionJSON.

<Media slots="video" width="750" height="500"/>

<https://youtu.be/giFJ6qbez_I?feature=shared>

## Implementation example

![alt image](spanielsBW.png?raw=true "Original Image")

In this example, we use a familiar asset and action file and modify the payload to return an output that executes all of the steps of the original action with one modification. Instead of color, we're going to use ActionJSON to return a black and white image. 

This full action file contains over 70 steps, so we don't show the entire JSON payload here. But you can see the part we modified to achieve the output below.

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/actionJSON \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [{
  "href": "<SIGNED_GET_URL>",
  "storage": "<storage>"
  }],
  "options": {
    "actionJSON": [{
        "_obj": "imageSize",
        "constrainProportions": true,
        "interfaceIconFrameDimmed": {
          "_enum": "interpolationType",
          "_value": "automaticInterpolation"
        },
        "scaleStyles": true
      }, {
        "_obj": "imageSize",
        "constrainProportions": true,
        "interfaceIconFrameDimmed": {
          "_enum": "interpolationType",
          "_value": "automaticInterpolation"
        },
        "resolution": {
          "_unit": "densityUnit",
          "_value": 72.0
        },
        "scaleStyles": true
      },
      {
        "_obj": "make",
        "_target": [{
          "_ref": "adjustmentLayer"
        }],
        "using": {
          "_obj": "adjustmentLayer",
          "type": {
            "_obj": "blackAndWhite",
            "blue": 20,
            "cyan": 60,
            "grain": 40,
            "magenta": 80,
            "presetKind": {
              "_enum": "presetKindType",
              "_value": "presetKindDefault"
            },
            "red": 40,
            "tintColor": {
              "_obj": "RGBColor",
              "blue": 179.00115966796876,
              "grain": 211.00067138671876,
              "red": 225.00045776367188
            },
            "useTint": false,
            "yellow": 60
          }
        }
      }
    ]
  },
  "outputs": [{
    "type": "image/jpeg",
    "storage": "<storage>",
    "href": "<SIGNED_POST_URL>"
  }]
}'
```

## Creating actionJSON files

### Setting up developer mode

To enable developer mode in your Photoshop app, follow these steps:

1. Navigate to:
    * Photoshop → Preferences → Plugins... (For Mac).
    * Edit → Preferences → Plugins... (For Windows).
  
2. Select *Enable Developer Mode*.
3. Quit Photoshop.
4. Reopen your Photoshop app with developer mode enabled.

If you're using Photoshop 23.4 (July 2022) or earlier, enable developer mode as a hidden feature by executing the command below.

For Mac:

  ```bash
  echo "UXPEnableScriptingUtilities 1" >>  "/Users/$USER/Library/Preferences/Adobe Photoshop 2021 Settings/PSUserConfig.txt"
  ```

For Windows Powershell:

  ```bash
  echo  "UXPEnableScriptingUtilities 1" >> "C:\Users\$env:USERNAME\AppData\Roaming\Adobe\Adobe Photoshop 2021\Adobe Photoshop 2021 Settings\PSUserConfig.txt"
  ```

### Creating new actionJSON

If you have developer mode enabled in Photoshop follow the instructions below. If you don't have developer mode enabled below please see the previous section.

1. Open the Photoshop app.
2. Select Settings → Plugins.
3. Select Development.
4. Select Record Action Commands....
5. Name your file and click **Save**. You can now make select actions in Photoshop such as resizing an image, adjusting hue and saturation and so on. Photoshop saves all of your actions in your new file.

Once you're done recording your action, you can stop recording and save:

1. Select Settings → Plugins.
2. Select Development.
3. Click **Stop Action Recording**.

Photoshop app saves your actions to the directory you chose when you named your file.

### Creating actionJSON in Actions Panel

You can alternatively create a new file in your Photoshop app's Action Panel:

1. Go to Windows → Actions. The action panel opens.
2. Select **New Action...** to create a new action, or click `+` in the panel.
  ![alt image](actions_panel_menu.png?raw=true "Original Image")
1. Select your action from the action set.
2. Select **Copy as Javascript**.
3. Paste the contents in any text editor.
4. Modify the file to trim out the actions.

Now you can use the action in your Photoshop API payload.

### Converting ATN files into actionJSON

This endpoint enables you to convert an *.atn* file to actionJSON format. This is the simplest and easiest way to create an actionJSON file.

### Converting ATN files into actionJSON with Photoshop

1. Go to Windows → Actions. The action panel opens.
2. Select **Load action**.
3. Choose the action you would like to convert to actionJSON.
4. Click on **Copy as Javascript**.
5. Paste the contents in any text editor.
6. Modify the file to trim out the actions obj blocks. An example is shown below in the code sample.

You can now use the action in your payload. 

Here is a code sample of Action JSON when you copy actions as Javascript from Photoshop:

```js
async function vignetteSelection() {
    let result;
    let psAction = require("photoshop").action;

    let command = [
        // Make snapshot
        {"_obj":"make","_target":[{"_ref":"snapshotClass"}],"from":{"_property":"currentHistoryState","_ref":"historyState"},"using":{"_enum":"historyState","_value":"fullDocument"}},
        // Feather
        {"descriptor": {"_obj":"feather","radius":{"_unit":"pixelsUnit","_value":5.0}}, "options": {"dialogOptions": "display"}},
        // Layer Via Copy
        {"_obj":"copyToLayer"},
        // Show current layer
        {"_obj":"show","null":[{"_enum":"ordinal","_ref":"layer","_value":"targetEnum"}],"toggleOptionsPalette":true},
        // Make layer
        {"_obj":"make","_target":[{"_ref":"layer"}]},
        // Fill
        {"_obj":"fill","mode":{"_enum":"blendMode","_value":"normal"},"opacity":{"_unit":"percentUnit","_value":100.0},"using":{"_enum":"fillContents","_value":"white"}},
        // Move current layer
        {"_obj":"move","_target":[{"_enum":"ordinal","_ref":"layer","_value":"targetEnum"}],"to":{"_enum":"ordinal","_ref":"layer","_value":"previous"}}
    ];
    result = await psAction.batchPlay(command, {});
}

async function runModalFunction() {
    await require("photoshop").core.executeAsModal(vignetteSelection, {"commandName": "Action Commands"});
}

await runModalFunction();
```

Modify the JavaScript file to trim out the actions. Remove everything else from the JavaScript file and copy the array containing `_obj` from the `command` variable, which will look similar to what's shown  below.

```js
[    
 {"_obj":"make","_target":[{"_ref":"snapshotClass"}],"from":{"_property":"currentHistoryState","_ref":"historyState"},
 "using":{"_enum":"historyState","_value":"fullDocument"}},
 {"_obj":"feather","radius":{"_unit":"pixelsUnit","_value":5.0}},
 {"_obj":"copyToLayer"},
 {"_obj":"show","null":[{"_enum":"ordinal","_ref":"layer","_value":"targetEnum"}],"toggleOptionsPalette":true},
 {"_obj":"make","_target":[{"_ref":"layer"}]},
 {"_obj":"fill","mode":{"_enum":"blendMode","_value":"normal"},"opacity":{"_unit":"percentUnit","_value":100.0},"using":{"_enum":"fillContents","_value":"white"},
 {"_obj":"move","_target":[{"_enum":"ordinal","_ref":"layer","_value":"targetEnum"}],"to":{"_enum":"ordinal","_ref":"layer","_value":"previous"}}
]
```

Find [details about actionJSON at Photoshop API, `batchPlay`][2].

### Executing an actionJSON with multiple inputs

With `/actionJSON` endpoint you can use multiple images to do compositing.

To supply multiple images and have it specified in the actionJSON, create a Placeholder Value in your actionJSON. The placeholder value must be `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_X` where `X` is the index of the `additionalImages` array.

For example, say an actionJSON requires two additional images:

* `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0` == `options.additionalImages[0]`
* `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_1` == `options.additionalImages[1]`

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/actionJSON \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs": [
    {
      "href": "<SIGNED_GET_URL>",
      "storage": "<storage>"
    }
  ],
  "options": {
    "additionalImages": [
      {
        "href": "<SIGNED_GET_URL>",
        "storage": "<storage>"
      }
    ],
    "actionJSON": [
    {
      "ID": 3,
      "_obj": "placeEvent",
      "freeTransformCenterState": {
        "_enum": "quadCenterState",
        "_value": "QCSAverage"
      },
      "null": {
        "_kind": "local",
        "_path": "ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0"
      },
      "offset": {
        "_obj": "offset",
        "horizontal": {
          "_unit": "pixelsUnit",
          "_value": 0
        },
        "vertical": {
          "_unit": "pixelsUnit",
          "_value": 0
        }
      }
    },
    {
      "_obj": "autoCutout",
      "sampleAllLayers": false
    },
    {
      "_obj": "make",
      "at": {
        "_enum": "channel",
        "_ref": "channel",
        "_value": "mask"
      },
      "new": {
        "_class": "channel"
      },
      "using": {
        "_enum": "userMaskEnabled",
        "_value": "revealSelection"
      }
    },
    {
      "_obj": "set",
      "_target": [
        {
          "_property": "selection",
          "_ref": "channel"
        }
      ],
      "to": {
        "_enum": "ordinal",
        "_value": "allEnum"
      }
    },
    {
      "_obj": "align",
      "_target": [
        {
          "_enum": "ordinal",
          "_ref": "layer"
        }
      ],
      "alignToCanvas": false,
      "using": {
        "_enum": "alignDistributeSelector",
        "_value": "ADSBottoms"
      }
    },
    {
      "_obj": "align",
      "_target": [
        {
          "_enum": "ordinal",
          "_ref": "layer"
        }
      ],
      "alignToCanvas": false,
      "using": {
        "_enum": "alignDistributeSelector",
        "_value": "ADSRights"
      }
    },
    {
      "_obj": "set",
      "_target": [
        {
          "_property": "selection",
          "_ref": "channel"
        }
      ],
      "to": {
        "_enum": "ordinal",
        "_value": "none"
      }
    }
  ]

  },
  "outputs": [
    {
      "type": "image/jpeg",
      "href": "<SIGNED_PUT_URL>",
      "storage": "<storage>"
    }
  ]
}'
```

<!-- Links -->
[1]: ../../guides/code_sample/index.md#executing-an-actionjson-with-multiple-inputs
[2]: https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/batchplay/
