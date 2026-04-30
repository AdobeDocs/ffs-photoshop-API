# Mask Body Parts API: Granular Labels

**USAGE GUIDE • ADOBE FIREFLY PHOTOSHOP API • MASK BODY PARTS — GRANULAR LABELS**

Feature Guide — `useGranularLabels` | API Version: v1 | April 2026

---

## 1. Overview

The Mask Body Parts API (`/v1/mask-body-parts`) detects and segments human body parts and clothing items in images, returning individual mask images for each identified region. By default, bilateral body parts (those that appear on both sides of the body) are returned as a single combined mask.

The granular labels feature extends this capability by returning side-specific masks for bilateral parts. When enabled, you receive separate, independent masks for the left and right instances of each applicable body part. This is controlled by the `useGranularLabels` boolean field in the request body.

---

## 2. When to Use Granular Labels

Use `useGranularLabels: true` when your workflow requires:

- **Independent per-limb compositing** — applying different shadow directions, reflections, or lighting effects to the left and right sides of a subject independently.
- **Ground shadow generation** — grounding individual feet or shoes for realistic shadow placement in sports and retail imagery.
- **Leg and foot reflection effects** — creating accurate mirror reflections for individual limbs without bleed from the opposite side.
- **High-volume automation** — processing large batches of sports player or product images where manual mask splitting is not feasible.
- **Precision apparel segmentation** — differentiating left/right sleeves, gloves, or shoes for e-commerce product presentation.

> ⚠️ If your workflow treats both sides of the body identically (e.g., full-body background removal), you do not need granular labels. Omit the flag or set it to `false` to use the standard, combined label set with lower response payload size.

---

## 3. API Reference

### Endpoint

```
POST https://image.adobe.io/v1/mask-body-parts
```

### Request Body Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `image` | object | Yes | The input image object. Contains `source` (URL) and `mediaType` fields. |
| `image.source.url` | string | Yes | Presigned URL of the input image. Max dimensions: 4000 x 4000 px. |
| `image.mediaType` | string | Yes | Media type of the input image. Accepted: `image/jpeg`, `image/png`. |
| `mask` | object | Yes | The subject mask object. Contains `source` (URL) and `mediaType` fields. |
| `mask.source.url` | string | Yes | Presigned URL of the subject mask image. Must be `image/png`. |
| `useGranularLabels` | boolean | No | When `true`, returns side-specific masks for bilateral body parts. Defaults to `false`. |

---

## 4. Request Examples

### Standard Request (Granular Labels Disabled)

```json
{
  "image": {
    "source": { "url": "https://storage.example.com/athlete.png" },
    "mediaType": "image/png"
  },
  "mask": {
    "source": { "url": "https://storage.example.com/athlete_mask.png" },
    "mediaType": "image/png"
  }
}
```

### Granular Labels Request

```json
{
  "image": {
    "source": { "url": "https://storage.example.com/athlete.png" },
    "mediaType": "image/png"
  },
  "mask": {
    "source": { "url": "https://storage.example.com/athlete_mask.png" },
    "mediaType": "image/png"
  },
  "useGranularLabels": true
}
```

---

## 5. Response Structure

The endpoint is asynchronous. The initial response is `202 Accepted` with a `jobId` and `statusUrl`. Poll the status endpoint until `status` is `succeeded`, then retrieve your `masks` array.

### Polling Status

```
GET https://image.adobe.io/v1/status/{jobId}
```

### Succeeded Response (Granular Labels)

```json
{
  "jobId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "status": "succeeded",
  "masks": [
    {
      "label": "Left Shoe",
      "score": 0.97,
      "boundingBox": { "left": 142, "top": 810, "width": 190, "height": 110 },
      "destination": { "url": "https://storage.adobe.io/..." },
      "mediaType": "image/png"
    },
    {
      "label": "Right Shoe",
      "score": 0.96,
      "boundingBox": { "left": 352, "top": 812, "width": 188, "height": 108 },
      "destination": { "url": "https://storage.adobe.io/..." },
      "mediaType": "image/png"
    },
    {
      "label": "Left Leg",
      "score": 0.98,
      "boundingBox": { "...": "..." },
      "destination": { "url": "https://storage.adobe.io/..." },
      "mediaType": "image/png"
    },
    { "label": "Right Leg", "...": "..." },
    { "label": "Upper Clothes", "...": "..." }
  ]
}
```

---

## 6. Granular Label Reference

The following labels may be returned in the `masks` array when `useGranularLabels` is `true`. Labels that are not bilateral (e.g., Face, Hair, Upper Clothes) are returned identically in both standard and granular modes.

| Body Region | Standard Labels | Granular Labels (New) |
| --- | --- | --- |
| Face / Head | Hair, Eyebrow, Eyes, Pupil, Nose, Mouth, Teeth, Face, Neck | Same (no change) |
| Beard | Beard | Same (no change) |
| Ears | Ear (combined) | **Left Ear, Right Ear** |
| Arms | Arm (combined) | **Left Arm, Right Arm** |
| Hands | Hand (combined) | **Left Hand, Right Hand** |
| Legs | Leg (combined) | **Left Leg, Right Leg** |
| Feet / Shoes | Feet / Shoe (combined) | **Left Shoe, Right Shoe** |
| Upper Apparel | Upper Clothes | Same (no change) |
| Lower Apparel | Lower Clothes | Same (no change) |
| Outerwear | Coat | Same (no change) |
| Dress | Dress | Same (no change) |
| Hat | Hat | Same (no change) |
| Glasses | Glasses | Same (no change) |
| Accessories | Accessories | Same (no change) |
| Background | Background | Same (no change) |

---

## 7. Best Practices

- Only enable `useGranularLabels` when your workflow requires left/right differentiation. The standard mode returns a smaller payload and may process faster.
- Ensure your input mask accurately covers the full subject. Poor subject masks may result in incomplete or merged left/right detections.
- Store masks by label from the response array — do not assume a fixed ordering. Always read the `label` field to identify each mask.
- For ground shadow workflows: use the `Left Shoe` and `Right Shoe` masks independently to calculate shadow anchor points per foot.
- For reflection workflows: mirror each shoe or leg mask individually along the vertical axis to create correct per-limb reflections.
- Input images should not exceed 4000 x 4000 px. For higher-resolution source images, downscale before calling the API.

---

## 8. Error Handling

| HTTP Code | `error_code` | Meaning / Action |
| --- | --- | --- |
| 400 | `input_validation_error` | Malformed request body. Check required fields and data types. |
| 401 | `unauthorized` | Missing or invalid bearer token. Re-authenticate. |
| 403 | `forbidden` | Valid token but insufficient permissions. Verify API entitlements. |
| 429 | `too_many_requests` | Rate limit exceeded. Implement exponential backoff. |
| 500 | `internal_server_error` | Transient server error. Retry with backoff before escalating. |

---

*Adobe Firefly Photoshop API — Mask Body Parts Granular Labels Guide • April 2026 • v1*
