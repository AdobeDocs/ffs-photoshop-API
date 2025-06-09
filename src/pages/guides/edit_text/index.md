---
title: Edit Text
description: Edit Text documentation
---

# Edit Text

The Edit Text endpoint supports editing one or more text layers within a PSD.

It enables users to:

* Format text properties such as anti-alias, orientation and be able to edit text contents. Changing only the text properties will not change any character paragraph styling.
* Some of the key character properties that can be formatted include (but not limited to):
  * Text treatments such as strike-through, underline, capitalization.
  * Character size and color.
  * Line and character spacing through leading, tracking, autoKern settings.
* All the paragraph properties are supported.
* Use custom fonts when specified through the `options.fonts` section in the API request body.

### Usage Recommendations

* Ensure that the input file is a PSD and that it contains one or more text layers.
* Refer to [Font Handling](#font-handling) and [Handle Missing Fonts](#handle-missing-fonts-in-the-document) more information.

You can find a code sample for making a text layer edit here:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/text \
  -H "Authorization: Bearer $token"  \
  -H "x-api-key: $apiKey" \
  -H "Content-Type: application/json" \
  -d '{
  "inputs":[
    {
      "href":"<SIGNED_GET_URL>",
      "storage":"<storage>"
    }
  ],
  "options":{
    "layers":[
      {
        "name": "My Text Layer",
        "text": {
            "content": "CHANGED TO NEW TEXT",
            "orientation": "horizontal",
            "characterStyles": [{
                "size": 15,
                "orientation": "horizontal",
                "color": {
                    "red":255,
                    "green":0,
                    "blue":0
                }
            }],
            "paragraphStyles": [{
              "alignment": "right"
            }]
        }
      }
    ]
  },
  "outputs":[
    {
      "href":"<SIGNED_POST_URL>",
      "storage":"<storage>",
      "type":"vnd.adobe.photoshop"
    }
  ]
}'
```

### Known Limitations

The API cannot automatically detect missing fonts in the layers. To prevent potential missing fonts from being replaced, please provide a `href` to the font in the `options.fonts` section of the API. For more details on specifying custom fonts, please refer to the example section below.

In this example, the font on the original image was altered using the Text API, as depicted in the image on the left:
![alt image](textlayer_example.png?raw=true "Original Image"). 