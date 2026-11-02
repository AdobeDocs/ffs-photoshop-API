---
title: Execute Actions — models reference
description: Models invoked by Execute Actions for Photoshop Services workloads (reference list).
hideBreadcrumbNav: true
keywords:
  - execute-actions
  - machine learning models
  - Photoshop Services
---

# Execute Actions — ML models reference

This page lists **models and cloud endpoints** used by **Execute Actions** when processing Photoshop Services.

## Model inventory

| Capability | Hosting | Model / identifier | API or endpoint | Notes |
| ---------- | ------- | ------------------ | --------------- | ----- |
| Generative Fill | Cloud | `me_md` | `https://firefly-clio-imaging.adobe.io/v2/images/fill` | Fill and expand each use the corresponding path. |
| Generative Expand | Cloud | `me_md` | `https://firefly-clio-imaging.adobe.io/v2/images/expand` | Fill and expand each use the corresponding path. |
| Generate Image (Text-to-Image) | Cloud | `clio3` | `https://firefly-clio-imaging.adobe.io/v2/images/generate` | Generates a new image from a text prompt only — no source image or mask/selection is sent. |
| Generate Similar | Cloud | `me_md` (routes to `clio3` if the target sheet wasn't originally generated via Fill/Expand) | `https://firefly-clio-imaging.adobe.io/v2/images/generate-similar` | Requires an existing generative sheet with at least one prior generated variation already on the target layer — it does not create one. |
| Gen Harmonize | Cloud | `gen_harmonize` | `https://di-imaging-genharm.ff.adobe.io/v2/images/harmonize` | Separate service host from the other Firefly/Clio endpoints above. |
| Select Subject | Cloud | Select Subject V5 | Generated dynamically | If cloud fails, falls back to **on-device** (uses **V3**). |
| Select Sky / sky replacement | On-device | `SKBS` / `SKRF` | — | |
| Remove tool — MetaCAF (generative remove) | Cloud | multi-edit erase | `https://di-me.ff.adobe.io/v2/images/generate-erase` | |
| People detection | On-device | `PeopleDistractorV1` | — | For **removal**, flow uses **generative remove (MetaCAF)** on **cloud**. |
| Wire removal | On-device | `WireGlobal`, `WireLocal`, `WireStuffSeg_V2`, `CMGAN_Tiny_V3` | — | All models used in the **same** pipeline. |
| Object selection | On-device | `object_selection`, `ultimate_universal_mask_refinement`, `select_subject_classifier` | — | All models used in the **same** pipeline. |
