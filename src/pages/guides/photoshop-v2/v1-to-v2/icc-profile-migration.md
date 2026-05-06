---
title: ICC Profile Migration Guide
description: Migrate to V2 ICC profile support for color management on output exports and document creation
hideBreadcrumbNav: true
keywords:
  - ICC profile
  - color management
  - sRGB
  - CMYK
  - custom profile
  - migration
  - v1 to v2
---

# ICC Profile Migration Guide

## Overview

ICC (International Color Consortium) profile support is a **new capability in Adobe Photoshop API V2**. The V1 API (`image.adobe.io`, `/pie/psdService/*`) did not support color profile configuration for outputs. When migrating to V2, you can now specify ICC profiles to control color management for your output exports (JPEG, PNG, TIFF, PSD).

This guide covers:

- Standard ICC profiles (predefined profiles)
- Custom ICC profiles (user-provided .icc files)
- Format support and restrictions
- Common validation errors and how to avoid them

## Summary of changes

| Change | V1 | V2 |
|--------|----|----|
| **ICC Profile Support** | Not available | Optional `iccProfile` on output exports and document creation |
| **Output Color Management** | N/A | Add `iccProfile` to any output (JPEG, PNG, TIFF, PSD) |
| **Document Creation Color Management** | N/A | Add `iccProfile` to `image` block in `/v2/create-composite` |

- **Conversion Behavior:** See [Format Support: Color Mode and Bit Depth](output-types-migration.md#format-support-color-mode-and-bit-depth) for details.

## Standard ICC profile

Standard profiles use predefined profile names. No external file is required.

### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be `"standard"` |
| `name` | string | Yes | One of the predefined profile names (see below) |
| `imageMode` | string | No | `"rgb"` or `"grayscale"`. Defaults to `"rgb"` for RGB profiles |

### Standard profile names

**RGB Profiles:**
- Adobe RGB (1998)
- Apple RGB
- ColorMatch RGB
- sRGB IEC61966-2.1

**Grayscale Profiles (Dot Gain):**
- Dot Gain 10%
- Dot Gain 15%
- Dot Gain 20%
- Dot Gain 25%
- Dot Gain 30%

**Grayscale Profiles (Gray Gamma):**
- Gray Gamma 1.8
- Gray Gamma 2.2

### Standard profile example

```json
"iccProfile": {
  "type": "standard",
  "name": "sRGB IEC61966-2.1",
  "imageMode": "rgb"
}
```

<InlineAlert variant="info" slots="text"/>

Profile names must match exactly (including spaces and punctuation). The `imageMode` for standard profiles is limited to `rgb` or `grayscale` — CMYK is not supported for standard profiles.

## Custom ICC profile

Custom profiles allow you to use your own .icc profile files. The file must be accessible via a URL (presigned URL, Creative Cloud path, etc.).

### Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Must be `"custom"` |
| `name` | string | Yes | Descriptive name for the profile (max 255 characters) |
| `source` | object | Yes | File reference with `url` (or Creative Cloud path) |
| `imageMode` | string | No | `"rgb"`, `"grayscale"`, or `"cmyk"` |

### Custom profile example

```json
"iccProfile": {
  "type": "custom",
  "name": "U.S. Web Coated (SWOP) v2",
  "imageMode": "cmyk",
  "source": {
    "url": "https://example.com/profiles/custom.icc"
  }
}
```

<InlineAlert variant="info" slots="text"/>

Custom profiles support CMYK via `imageMode: "cmyk"`, which is not available for standard profiles.

## Format support

ICC profiles are supported for the following output formats:

| Format | mediaType | ICC Profile Supported |
|--------|-----------|----------------------|
| JPEG | `image/jpeg` | Yes |
| PNG | `image/png` | Yes |
| TIFF | `image/tiff` | Yes |
| PSD | `image/vnd.adobe.photoshop` | Yes |
| PSDC | `document/vnd.adobe.cpsd+dcxucf` or `document/vnd.adobe.cpsd+dcx` | **No** |

### PSDC restriction

ICC profiles are **not** supported for PSDC (Photoshop Cloud Document) output format. If you include `iccProfile` with a PSDC output, you will receive:

> ICC profiles are not currently supported for PSDC (Photoshop Cloud Document) output format. Please remove the iccProfile field or use a different output format (JPEG, PNG, TIFF, or PSD) if ICC profile support is required.

**Solution:** Remove the `iccProfile` field from PSDC outputs, or use JPEG, PNG, TIFF, or PSD instead.

## Where ICC profile applies

### On outputs (export color management)

Add `iccProfile` to any output in these endpoints:

- `/v2/create-composite`
- `/v2/create-artboard`
- `/v2/execute-actions`

```json
{
  "outputs": [
    {
      "destination": { "url": "https://example.com/output.jpg" },
      "mediaType": "image/jpeg",
      "iccProfile": {
        "type": "standard",
        "name": "Adobe RGB (1998)",
        "imageMode": "rgb"
      }
    }
  ]
}
```

### On the `image` block (document creation color management)

When creating a new document via `/v2/create-composite` (no `image.source`), add `iccProfile` to the `image` block to set the document's embedded color profile at creation time. Both standard and custom profiles are supported:

```json
{
  "image": {
    "width": 1920,
    "height": 1080,
    "resolution": {"unit": "density_unit", "value": 72},
    "mode": "rgb",
    "depth": 8,
    "iccProfile": {
      "type": "custom",
      "name": "DCI P3 D65",
      "source": { "url": "https://example.com/profiles/DCI-P3-D65.icc" },
      "imageMode": "rgb"
    }
  },
  "outputs": [
    {
      "destination": { "url": "https://example.com/output.psd" },
      "mediaType": "image/vnd.adobe.photoshop"
    }
  ]
}
```

<InlineAlert variant="info" slots="text"/>

`iccProfile` on the `image` block sets the document's embedded profile. `iccProfile` on an `output` converts the exported file's color space. Both can be used independently or together.

## Complete examples

### Create composite with standard ICC profile

```json
{
  "image": {
    "source": { "url": "https://example.com/input.psd" }
  },
  "outputs": [
    {
      "destination": { "url": "https://example.com/output.psd" },
      "mediaType": "image/vnd.adobe.photoshop",
      "iccProfile": {
        "type": "standard",
        "name": "sRGB IEC61966-2.1",
        "imageMode": "rgb"
      }
    }
  ]
}
```

### Create composite with custom ICC profile (CMYK)

```json
{
  "image": {
    "source": { "url": "https://example.com/input.psd" }
  },
  "outputs": [
    {
      "destination": { "url": "https://example.com/output.tiff" },
      "mediaType": "image/tiff",
      "iccProfile": {
        "type": "custom",
        "name": "U.S. Web Coated (SWOP) v2",
        "imageMode": "cmyk",
        "source": { "url": "https://example.com/profiles/custom.icc" }
      }
    }
  ]
}
```

## Common migration errors

### Error 1: PSDC with ICC profile

**Problem:**

```json
{
  "mediaType": "document/vnd.adobe.cpsd+dcx",
  "iccProfile": {
    "type": "standard",
    "name": "sRGB IEC61966-2.1",
    "imageMode": "rgb"
  }
}
```

**Error:**
> ICC profiles are not currently supported for PSDC (Photoshop Cloud Document) output format. Please remove the iccProfile field or use a different output format (JPEG, PNG, TIFF, or PSD) if ICC profile support is required.

**Solution:** Remove `iccProfile` from PSDC outputs, or switch to JPEG, PNG, TIFF, or PSD.

### Error 2: Uppercase imageMode

**Problem:**

```json
"iccProfile": {
  "type": "standard",
  "name": "sRGB IEC61966-2.1",
  "imageMode": "RGB"
}
```

**Error:**
> Invalid value 'RGB' at path 'outputs[0].iccProfile.imageMode'. Accepted values are: rgb, grayscale

**Solution:** Use lowercase values only: `"rgb"`, `"grayscale"`, or `"cmyk"` (for custom profiles).

### Error 3: Standard profile with imageMode cmyk

**Problem:**

```json
"iccProfile": {
  "type": "standard",
  "name": "sRGB IEC61966-2.1",
  "imageMode": "cmyk"
}
```

**Error:**
> Invalid standard ICC profile image mode

**Solution:** Standard profiles only support `rgb` or `grayscale`. Use a custom profile with `imageMode: "cmyk"` for CMYK workflows.

### Error 4: Invalid standard profile name

**Problem:**

```json
"iccProfile": {
  "type": "standard",
  "name": "SRGB_IEC61966_2_1",
  "imageMode": "rgb"
}
```

**Error:**
> Unknown standard ICC profile name: SRGB_IEC61966_2_1

**Solution:** Use the exact display name: `"sRGB IEC61966-2.1"` (with spaces and hyphen).

### Error 5: Custom profile name exceeds 255 characters

**Problem:**

```json
"iccProfile": {
  "type": "custom",
  "name": "A very long profile name that exceeds 255 characters...",
  "source": { "url": "https://example.com/profile.icc" }
}
```

**Error:**
> ICC profile name must not exceed 255 characters

**Solution:** Shorten the profile name to 255 characters or less.

### Error 6: Wrong spelling for grayscale

**Problem:**

```json
"iccProfile": {
  "type": "standard",
  "name": "sRGB IEC61966-2.1",
  "imageMode": "greyscale"
}
```

**Error:**
> Invalid value 'greyscale' at path 'outputs[0].iccProfile.imageMode'. Accepted values are: rgb, grayscale

**Solution:** The API uses American spelling: `"grayscale"` (not `"greyscale"`).

## Migration checklist

Use this checklist when adding ICC profile support in V2:

### General

- [ ] ICC profile is optional — only add if you need color management
- [ ] Use `iccProfile` on outputs for JPEG, PNG, TIFF, or PSD (not PSDC)

### Standard profiles

- [ ] Use exact profile names (e.g., `"sRGB IEC61966-2.1"`)
- [ ] Use `imageMode: "rgb"` or `"grayscale"` only (no CMYK)
- [ ] Use lowercase for `imageMode`

### Custom profiles

- [ ] Provide `name` (max 255 characters) and `source.url`
- [ ] Use `imageMode: "rgb"`, `"grayscale"`, or `"cmyk"` as needed
- [ ] Use lowercase for `imageMode`
- [ ] Ensure the profile URL is accessible (presigned, etc.)

### Validation

- [ ] Do not use `iccProfile` with PSDC outputs
- [ ] Verify `imageMode` values are lowercase

## Quick reference

### Standard profile names

| Category | Names |
|----------|-------|
| RGB | Adobe RGB (1998), Apple RGB, ColorMatch RGB, sRGB IEC61966-2.1 |
| Grayscale (Dot Gain) | Dot Gain 10%, 15%, 20%, 25%, 30% |
| Grayscale (Gamma) | Gray Gamma 1.8, Gray Gamma 2.2 |

### imageMode values

| Profile Type | Allowed Values |
|--------------|----------------|
| Standard | `rgb`, `grayscale` |
| Custom | `rgb`, `grayscale`, `cmyk` |

### Format support

| Format | ICC Supported |
|--------|---------------|
| JPEG, PNG, TIFF, PSD | Yes |
| PSDC | No |

## Related migration guides

- [Output Types Migration](output-types-migration.md) - JPEG, PNG, PSD, TIFF output format changes
- [Composite Migration](composite-migration.md) - Layer operations in create-composite
- [Migration Quick Reference](index.md) - Complete V1 to V2 migration overview
