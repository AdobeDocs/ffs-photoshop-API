---
title: Photoshop API Usage Notes
description: This document has details about what's currently supported, limitations, and workarounds for the Photoshop APIs.
contributors:
  - https://github.com/AEAbreu-hub
---

# Audio/Video API Usage Notes

This document has details about what's currently supported, limitations, and workarounds for the Photoshop APIs to help developers optimize their API implementations and understand service boundaries.

## Smart Object

Here's the technical usage information for the Text-to-Speech API.

### Limitations and workarounds

- **TTS voice modulation**: The output may have signification modulation in pitch or voice. Regenerating the audio can often resolve this issue.
- **Limited voice controls**: Currently voice controls like emphasis, speed or pitch modulation aren't supported.
- **Mispronunciation**: The audio output might mispronounce certain uncommon words or proper nouns. This can be addressed by using phonetic spellings.

### Text input specifications

**Transcript length**: Up to ```20000``` characters.

**Input format**: Plain text, or ```.txt``` file via a pre-signed URL.

### API render time

Render times for Text-to-speech are 2X the output audio length.

### Request limits

To be sure everyone enjoys peak performance with these APIs, Adobe sets limits on the volume, frequency, and concurrency of API calls. Adobe monitors your API usage and will contact you proactively to resolve any risks to API performance.

<InlineAlert variant="warning" slots="text" />

Be aware that these usage limits apply to your entire organization.

These are the current rate limits for API requests:

**Get Voices API (/voices)**: 50 requests per minute.

**Generate Speech API (/generate-speech)**: 10 requests per minute.

You may encounter a `HTTP 429 "Too Many Requests"` error if usage exceeds either the per minute or per day limits. We recommend using the `retry-after` header to determine the number of seconds you should wait before trying again.

## Reframe API usage

### Supported media properties

| Attribute | Input | Output |
|-----------|--------|--------|
| Formats | Video: .mp4, .mov; Image: .png, .gif | .mp4 |
| Upload/Download type | Pre-signed URLs to individual videos, overlays | Pre-signed URLs to individual videos |
| Video Duration (Max) | 30 minutes | Same as source |
| Video Size (Max) | 10 GB | Same as source |
| Video Codecs | H.265/HEVC (only 4:2:0), H.264/AVC | Same as source |
| Color Properties | BT 601, BT 709, BT 2020, BT 2020 HLG, BT 2020 PQ | Same as source |
| Frame Rate | 24, 25, 29.97, 30, 50, 59.94, 60 | Same as source |
| 4K Support | Yes | Yes |

### Performance characteristics

| Configuration                                     | Estimated Render Time                 |
|-------------------------------                    |---------------------------------------|
| 1 aspect ratio requested, 60s input video, Scene Edit Detection NOT applied   | ~0.5x video length  |
| 5 aspect ratios requested, 60s input video, Scene Edit Detection NOT applied  | ~0.6x video length |
| 1 aspect ratio requested, 60s input video, Scene Edit Detection applied         | ~1.3x video length        |
| 5 aspect ratios requested, 60s input video, Scene Edit Detection applied         | ~1.5x video length        |

### Request limits

To ensure equitable peak performance, Adobe limits the volume, frequency, and concurrency of API calls. We monitor usage to proactively resolve any risks to performance.

These are the current rate limits for API requests:

**Reframe Processing API (/reframe)**: Max of 2 requests per minute.

You'll encounter a HTTP 429 "Too Many Requests" error if usage exceeds the limits per minute or per day.
We recommend using the 'retry-after' header to determine the number of seconds you should wait before trying again.

## Translate and Lip Sync API usage

### Known limitations and workarounds

- **Speaker Mismatch:** Speaker mismatches or additional/missing speakers may occasionally occur in output transcripts. This has been observed in approximately 9% of cases. Content where speakers overlap may not produce the best results and should be avoided.
- **Voice Modulation:** Voices in the output may vary in pitch or show significant modulation. Regenerating the video/audio can often resolve this issue.
- **Re-dubbing Dubbed Content:** Avoid using deepfake content for re-dubbing purposes.
- **Singing Isn't Supported:** A music video or a song won't be dubbed correctly.

### For editing transcripts

Only sentence editing is currently supported. Do not modify the timestamps.

Speakers can be updated, however don't remove speakers before dubbing. Also, dub using the edited transcripts in different target languages.

### Language support

Dubbing is supported for the following languages:

- English (Indian) (`en-IN`)
- English (American) (`en-US`)
- English (British) (`en-GB`)
- Spanish (Spanish) (`es-ES`)
- Spanish (Argentina) (`es-AR`)
- Spanish (Latin America) (`es-419`)
- French (France) (`fr-FR`))
- French (Canada) (`fr-CA`)
- Danish (Denmark) (`da-DK`)
- Norwegian (Norway) (`nb-NO`)
- German (`de-DE`)
- Italian (`it-IT`)
- Portuguese (Brazil) (`pt-BR`)
- Portuguese (Portugal) (`pt-PT`)
- Hindi (India) (`hi-IN`)
- Japanese (Japan) (`ja-JP`)
- Korean (South Korea) (`ko-KR`)

### Input video support

Technical details for videos used as input:

- **Duration (max):** 30 mins
- **FPS:** 24 fps, 25 fps, 29.97, 30, 50, 59.94, 60
- **Resolution (max):** Full HD `1920*1080px` or `1080*1920px`
- **CODEC**: `H.264, HEVC`
- **Formats/container:** `.mp4, .mov`
- **Input medium:** Pre-signed URL
- **Render time:** 3x the video length, 10x the video length (for 30 fps and 1080 resolution) if `lipSync` is enabled
- **Speaker speech (min):** 5 secs
- **Dubbing and Lip Sync:** Multi-speaker support

### Input audio support

Technical details for audio used as input:

- **Duration (max):** 30 mins
- **CODEC:** `MPEG, PCM`
- **Formats/container:** `.mp3, .wav, .aac`
- **Input medium:** Pre-signed URL
- **Render time:** 3x the audio length
- **Dubbing:** Multi-speaker support

### Request limits

To ensure equitable peak performance, Adobe places limits on the volume, frequency, and concurrency of API calls, and monitors API usage to proactively resolve any risks to performance.

<InlineAlert variant="warning" slots="text1" />

These usage limits apply to your entire organization. <br/>

The current limitations are:

**Transcribe endpoint (/transcribe):** 5 requests per minute.

**Dubbing/Lip Sync endpoint (/dub):**  5 requests per minute and 150 requests per day.

## GET status API

### Request limits

**Get Result endpoint (/status/{jobId}):** 100 requests per minute.
