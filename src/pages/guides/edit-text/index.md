---
title: Edit Text
description: Learn how to edit text layers in Photoshop files using the Edit Text API endpoint to modify text content, formatting, and styling
hideBreadcrumbNav: true
keywords:
  - edit text
  - text layers
  - text formatting
  - font handling
  - PSD files
contributors:
  - https://github.com/AEAbreu-hub
---

# Edit text

The Edit Text endpoint allows you to modify text layers within Photoshop files (PSD files).

In these example images, we've altered the font on the original image (on the left) using the Text API:

![alt image](textlayer_example.png?raw=true "Original Image")

The Edit Text endpoint supports editing one or more text layers within a PSD. Users can:

<ListBlock slots="text1, text2" repeat="5" iconColor="#2ac3a2" icon="checkmark" variant="fullWidth" />

Format text properties such as anti-alias, orientation and edit text contents. Only changing the text properties won't change styling.
  
Use custom fonts, specified in the API request body.
  
Edit the text contents.
  
Change the font.
  
Edit font size.
  
Change the font color to RGB, CMYK, grayscale, or lab.
  
Edit the text orientation (horizontal/vertical).
  
Edit the paragraph alignment, such as left, center, right, justify, justify left, justify center, and justify right.

Add text treatments like strike-through, underline, and capitalization.

Format line and character spacing through leading, tracking, and autoKern settings.

## Known limitations

* The API can't automatically detect missing fonts in the layers. To prevent potentially missing fonts from being replaced, provide an `href` to the font in `options.fonts`. For more details on specifying custom fonts, see the [Font handling](#font-handling) section.
* Ensure that the input file is a PSD and that it contains one or more text layers.
* Some text attributes (for example, tracking, leading, and kerning) don't retain their original values.

## Font handling

To correctly operate on text layers, the fonts needed for those layers need to be available when processing the PSD.

Reference fonts in the API request using the correct Postscript name for that font. Using any other name causes the API to treat this as a missing font.

To use a custom font you must include an href to the font in the API request `inputs`, in this format: `<font_postscript_name>.<ext>`.

**Example**

  ```js
  {
    "storage": "external",
    "href": "<STORAGE_URL_TO_OPEN_SANS_CONDENSED_LIGHT_TTF>"
  }
  ```

### Handling missing fonts

Use the `manageMissingFonts` field in the `options` of the request to specify how to handle missing fonts. There are two accepted values:

* `fail` to force the request/job to fail.
* `useDefault` to use the system designated default font: `ArialMT`.

Or specify a global font in the `globalFont` field in the `options` section of the request, which would act as a default font for the current request.

<InlineAlert variant="info" slots="header, text1" />

NOTE

With an OAuth integration, Adobe Fonts can be used as a global font as well. If the global font is a custom font, upload it to a supported cloud storage type and specify the `href` and `storage` type in the `options.fonts` section of the request.

### Supported fonts

The supported Postscript fonts are:

|                                   |
|---------------------------------- |
| AcuminVariableConcept             |
| AdobeArabic-Bold                  |
| AdobeArabic-BoldItalic            |
| AdobeArabic-Italic                |
| AdobeArabic-Regular               |
| AdobeDevanagari-Bold              |
| AdobeDevanagari-BoldItalic        |
| AdobeDevanagari-Italic            |
| AdobeDevanagari-Regular           |
| AdobeFanHeitiStd-Bold             |
| AdobeGothicStd-Bold               |
| AdobeGurmukhi-Bold                |
| AdobeGurmukhi-Regular             |
| AdobeHebrew-Bold                  |
| AdobeHebrew-BoldItalic            |
| AdobeHebrew-Italic                |
| AdobeHebrew-Regular               |
| AdobeHeitiStd-Regular             |
| AdobeMingStd-Light                |
| AdobeMyungjoStd-Medium            |
| AdobePiStd                        |
| AdobeSongStd-Light                |
| AdobeThai-Bold                    |
| AdobeThai-BoldItalic              |
| AdobeThai-Italic                  |
| AdobeThai-Regular                 |
| CourierStd                        |
| CourierStd-Bold                   |
| CourierStd-BoldOblique            |
| CourierStd-Oblique                |
| EmojiOneColor                     |
| KozGoPr6N-Bold                    |
| KozGoPr6N-Medium                  |
| KozGoPr6N-Regular                 |
| KozMinPr6N-Regular                |
| MinionPro-Regular                 |
| MinionVariableConcept-Italic      |
| MinionVariableConcept-Roman       |
| MyriadArabic-Bold                 |
| MyriadArabic-BoldIt               |
| MyriadArabic-It                   |
| MyriadArabic-Regular              |
| MyriadHebrew-Bold                 |
| MyriadHebrew-BoldIt               |
| MyriadHebrew-It                   |
| MyriadHebrew-Regular              |
| MyriadPro-Bold                    |
| MyriadPro-BoldIt                  |
| MyriadPro-It                      |
| MyriadPro-Regular                 |
| MyriadVariableConcept-Italic      |
| MyriadVariableConcept-Roman       |
| NotoSansKhmer-Regular             |
| NotoSansLao-Regular               |
| NotoSansMyanmar-Regular           |
| NotoSansSinhala-Regular           |
| SourceCodeVariable-Italic         |
| SourceCodeVariable-Roman          |
| SourceSansVariable-Italic         |
| SourceSansVariable-Roman          |
| SourceSerifVariable-Roman         |
| TrajanColor-Concept               |

## Implementation examples

### Making a text layer edit

This code sample makes a text layer edit:

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

### Editing two text layers

This example applies edits to two text layers:

```shell
curl -X POST \
  https://image.adobe.io/pie/psdService/text \
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
    "fonts": [
      {
        "storage": "<storage>",
        "href": "<SIGNED_GET_URL>"
      }
    ],
    "layers": [
      {
        "name": "<name_of_text_layer_1_to_edit>",
        "text": {
            "orientation": "horizontal",
            "contents": "New text Contents 1",
            "antiAlias": "antiAliasSharp",
            "characterStyles": [{
              "autoKern": "metricsKern",
              "fontPostScriptName": "<font_postscript_name>",
              "fontCaps": "allCaps",
              "size": 25,
              "leading": 20,
              "tracking": 20,
              "syntheticBold": true,
              "ligature": true,
              "syntheticItalic": true,
              "color": {
                "blue": 100,
                "green": 200,
                "red": 163
              }
            }],
            "paragraphStyles": [{
              "align": "right"
            }]
        }
      },
      {
        "name": "<name_of_text_layer_2_to_edit>",
        "text": {
          "contents": "New text Contents 2",
          "characterStyles": [{
              "size": 45,
              "stylisticAlternates": true,
              "leading": 100,
              "tracking": 100,
              "baseline": "subScript",
              "strikethrough": true,
              "underline": true,
              "verticalScale": 150,
              "horizontalScale": 200,
              "color": {
                "blue": 300,
                "green": 100,
                "red": 63
              }
            }]
        }
      }
    ]
  },
  "outputs": [
    {
      "href": "<SIGNED_POST_URL>",
      "type": "vnd.adobe.photoshop",
      "storage": "<storage>"
    }
  ]
}'
```

### Changing the font in a text layer

This example changes the font in a text layer named `My Text Layer` to a custom font `VeganStylePersonalUse`. The value for the `fontName` field in the `text.characterStyles` section is the full Postscript name of the custom font:

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
    "fonts": [
      {
        "storage": "<storage>",
        "href": "<SIGNED_GET_URL_TO_VeganStylePersonalUse.ttf>"
      }
    ],
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
