---
title: "/v2/edit API Benchmarking"
description: Benchmarking tables for Photoshop POST /v2/edit JPEG and PNG outputs by resolution, quality, and compression for capacity planning.
hideBreadcrumbNav: true
keywords:
  - benchmarks
  - Photoshop API
  - Photoshop Services
  - v2 edit
  - POST /v2/edit
  - latency
  - JPEG
  - PNG
  - quality
  - compression
  - performance
---

# /v2/edit API Benchmarking

The tables below present **benchmarking results for unified API workloads** for asynchronous jobs completed via **POST /v2/edit** on the Photoshop APIs, for raster output at fixed image dimensions, broken out by JPEG `quality` and PNG `compression` in the request output options. Use them for **capacity planning and rough expectations**; they are **not** a performance SLA. Actual job time depends on which adjustments you apply, source imagery, I/O, and load.

For endpoint usage and adjustment parameters, see [Edit Operations Migration](../edit-operations.md).

<InlineAlert variant="info" slots="header, text1" />

Note

These figures are illustrative benchmark results. They do not guarantee processing time for your workloads or environment.

## JPEG output (seconds)

The values correspond to JPEG `input` and JPEG `output` using the `quality` settings `poor`, `medium`, and `photoshop_max`. See [Output Types Migration](../output-types-migration.md) for all supported `quality` values and defaults.

### JPEG chart

![Line chart: JPEG output latency in seconds versus image resolution for POST /v2/edit, series for quality poor, medium, and photoshop_max](../../../../assets/v2-edit-jpeg-benchmarking.png?raw=true)

*Chart series match the table columns below. Axis units are seconds.*

| Resolution | `poor` | `medium` | `photoshop_max` |
| ---------- | -----: | -------: | --------------: |
| 640×640 | 0.789 | 0.945 | 0.876 |
| 800×600 | 0.848 | 0.858 | 0.800 |
| 1024×768 | 0.755 | 0.788 | 0.742 |
| 1280×720 | 0.774 | 0.805 | 0.808 |
| 1080×1080 | 0.817 | 0.877 | 0.894 |
| 1920×1080 | 0.939 | 0.888 | 1.046 |
| 2160×3840 | 1.288 | 1.300 | 1.430 |
| 3840×2160 | 1.248 | 1.341 | 1.387 |
| 4000×3000 | 1.579 | 1.637 | 1.913 |
| 5120×2880 | 1.723 | 1.819 | 2.202 |
| 4000×4000 | 2.057 | 1.966 | 2.486 |
| 6000×4000 | 2.229 | 2.300 | 2.826 |
| 4320×7680 | 3.094 | 2.986 | 3.855 |
| 7680×4320 | 3.081 | 3.140 | 3.945 |
| 6000×6000 | 3.497 | 3.345 | 4.116 |
| 7500×5000 | 3.284 | 3.662 | 4.198 |
| 8200×5120 | 3.807 | 3.753 | 4.584 |
| 8000×6000 | 4.272 | 4.011 | 5.367 |
| 7872×7872 | 5.292 | 5.326 | 6.550 |
| 7990×7926 | 5.401 | 5.603 | 6.446 |

## PNG output (seconds)

The values correspond to PNG `input` and PNG `output` using the `compression` settings `none`, `default`, and `maximum`. See [Output Types Migration](../output-types-migration.md) for all supported `compression` values and defaults.

### PNG chart

![Line chart: PNG output latency in seconds versus image resolution for POST /v2/edit, series for compression none, default, and maximum](../../../../assets/v2-edit-png-benchmarking.png?raw=true)

*Chart series match the table columns below. Axis units are seconds.*

| Resolution | `none` | `default` | `maximum` |
| ---------- | -----: | --------: | ----------: |
| 640×640 | 1.253 | 0.989 | 1.244 |
| 800×600 | 0.988 | 1.008 | 1.164 |
| 1024×768 | 0.872 | 1.144 | 1.605 |
| 1280×720 | 0.824 | 1.113 | 1.541 |
| 1080×1080 | 1.099 | 1.149 | 1.926 |
| 1920×1080 | 1.156 | 1.569 | 2.891 |
| 2160×3840 | 1.897 | 3.788 | 11.174 |
| 3840×2160 | 2.048 | 3.732 | 9.369 |
| 4000×3000 | 2.500 | 5.470 | 14.948 |
| 5120×2880 | 2.660 | 5.981 | 19.766 |
| 4000×4000 | 3.471 | 7.359 | 21.271 |
| 6000×4000 | 4.728 | 10.693 | 37.174 |
| 4320×7680 | 5.706 | 12.697 | 49.087 |
| 7680×4320 | 4.411 | 12.881 | 55.451 |
| 6000×6000 | 5.261 | 14.899 | 59.810 |
| 7500×5000 | 5.305 | 15.386 | N/A |

**N/A:** The job **timed out** and the request **could not be completed** under the benchmark conditions for PNG `maximum` at that resolution.
Note: Resolution 7500×5000 and higher will timeout.

## Reading the numbers

PNG **`maximum`** compression increases encode time sharply at large resolutions compared to **`default`**. At the largest sizes, **`maximum`** may exceed job time limits for **`/v2/edit`** jobs (shown as **N/A**). For very large exports, prefer **`default`** or a lower compression level if you need reliable completion within typical job timeouts. For service limits, retries, and related behavior, see [Technical Usage Notes](/getting-started/technical-usage-notes/index.md).
