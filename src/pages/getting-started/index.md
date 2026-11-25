---
title: Getting Started
description: Authenticate, prepare a file, submit a Photoshop API request, and check the result.
keywords:
  - getting started
  - authentication
  - access token
  - generate manifest
  - job status
hideBreadcrumbNav: true
contributors:
  - https://github.com/khound
  - https://github.com/archyposada
  - https://github.com/AEAbreu-hub
---

# Getting Started

Make your first Photoshop API call: generate a manifest that lists a PSD's
document properties and layers. Complete the steps in order; each step uses
values from the previous one.

## About Server-to-Server Authentication

For your application to generate an access token, an end user doesn't need to sign in or provide consent to your application. Instead, your application can use its credentials (Client ID and Secret) to authenticate itself and generate access tokens. Your application can then use these to call Adobe APIs and services on its behalf.

This is sometimes referred to as "two-legged OAuth".

Automate your token generation by calling the endpoint using standard OAuth2 libraries. Using industry-standard libraries is the quickest and most secure way of integrating with OAuth. Be diligent when choosing the OAuth 2.0 library that works best for your application. Your teams' projects likely leverage OAuth libraries already to connect with other APIs. It's recommended to use these libraries to automatically generate tokens when they expire.


## Before You Start

You need:

- An [Adobe Developer Console][console] project with Photoshop API
  [OAuth Server-to-Server credentials][s2s], under an Enterprise contract that
  includes Firefly Services. Your Adobe representative can help.
- An [Adobe Developer Console account][console] and a
  [project][console-project] with the credentials configured.
- The project's **Client ID** and **Client Secret**. Keep them out of
  client-side code, logs, and source control.
- A PSD that you have permission to process.

## 1. Authenticate

1. Export your credentials in a secure terminal:

    ```bash
    export PS_FF_SERVICES_CLIENT_ID=<CLIENT_ID>
    export PS_FF_SERVICES_CLIENT_SECRET=<CLIENT_SECRET>
    ```

2. Request an access token:

    ```bash
    curl -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'grant_type=client_credentials' \
      -d "client_id=$PS_FF_SERVICES_CLIENT_ID" \
      -d "client_secret=$PS_FF_SERVICES_CLIENT_SECRET" \
      -d 'scope=openid,AdobeID,read_organizations'
    ```

    ```json
    {
      "access_token": "<ACCESS_TOKEN>",
      "token_type": "bearer",
      "expires_in": 86399
    }
    ```

    | JSON Path | Type | Presence | Meaning |
    |---|---|---|---|
    | `access_token` | string | Always | Token for the `Authorization` header. |
    | `expires_in` | integer | Always | Seconds until the token expires. |
    | `token_type` | string | Always | Always `bearer`. |

3. Export the token:

    ```bash
    export PS_FF_SERVICES_ACCESS_TOKEN=<ACCESS_TOKEN>
    ```

Send these headers with every request:

| Header | Required | Value |
|---|---|---|
| `Authorization` | Yes | `Bearer` followed by the access token. |
| `Content-Type` | For `POST` | `application/json` |
| `x-api-key` | Yes | Your Client ID. |

Request a new token before `expires_in` elapses. You can also
[generate a token in the Developer Console][console-token].

## 2. Prepare Input and Output Locations

1. Create a signed `GET` URL for your PSD. It must use HTTPS and stay valid
   until the job finishes. See [Create Signed URLs][signed-urls] and
   [URL Requirements][url-requirements].
2. Choose an output destination. This quick start returns the manifest in the
   status response, so it needs no output storage. For files such as images,
   see [Choose A Destination][destinations].

To read input from Creative Cloud storage instead of a URL, see
[Specify A Source][sources].

## 3. Submit a Request

1. Replace `<SIGNED_GET_URL>` with your PSD's URL and submit the request:

    ```shell
    curl -i -X POST https://photoshop-api.adobe.io/v2/generate-manifest \
      -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
      -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "image": { "source": { "url": "<SIGNED_GET_URL>" } },
        "outputs": [
          { "destination": { "embedded": "json" }, "mediaType": "application/json" }
        ]
      }'
    ```

    | Field | Type | Required | Default | Meaning and Constraints |
    |---|---|---|---|---|
    | `image` | object | Yes | None | The input document. |
    | `image.source` | object | Yes | None | Where to read the input. See [Specify A Source][sources]. |
    | `image.source.url` | string | Yes, for a URL source | None | Signed HTTPS URL of the PSD. |
    | `outputs` | array of object | Yes | None | One to 25 outputs. See [Output Object][output-object]. |
    | `outputs[].destination` | object | Yes | None | Where to return the output. See [Embedded Destination][embedded]. |
    | `outputs[].destination.embedded` | string | Yes, for an embedded destination | None | Values: `base64`, `json`, `string`. Use `json` to return the manifest as an object. |
    | `outputs[].mediaType` | string | No | `application/json` | Values: `application/json`. |

2. Confirm the response status is `202 Accepted`. If the response includes a
   `Retry-After` header, wait for that many seconds before polling. Otherwise,
   wait 2 seconds before the first poll. The body includes `statusUrl`:

    ```json
    {
      "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
      "statusUrl": "https://photoshop-api.adobe.io/v2/status/de2415fb-82c6-47fc-b102-04ad651c5ed4"
    }
    ```

    | JSON Path | Type | Presence | Meaning |
    |---|---|---|---|
    | `jobId` | string | Always | Identifier of the accepted job (UUID). |
    | `statusUrl` | string | Always | URL to poll for this job's status. |

A `202` means the request was accepted, not that the job succeeded. Any other
status means no job was created; see [Errors and Limits][errors].

## 4. Check the Result

1. If the `202` response included `Retry-After`, wait for that many seconds.
   Otherwise, wait 2 seconds before polling.
2. Request the job status:

    ```shell
    curl -X GET "<STATUS_URL>" \
      -H "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
      -H "x-api-key: $PS_FF_SERVICES_CLIENT_ID"
    ```

3. While `status` is `not_started` or `running`, increase the interval between
   polls up to 30 seconds, then repeat step 2.
4. When `status` is `succeeded`, read the manifest from
   `result.outputs[0].destination.content`. This excerpt omits fields:

    ```json
    {
      "jobId": "de2415fb-82c6-47fc-b102-04ad651c5ed4",
      "status": "succeeded",
      "result": {
        "outputs": [
          {
            "destination": {
              "content": {
                "document": {
                  "bounds": { "left": 0, "top": 0, "right": 1000, "bottom": 1000 },
                  "depth": 8,
                  "imageMode": "rgb"
                },
                "layers": [
                  { "id": 1, "index": 0, "name": "Background", "type": "background_layer", "visible": true }
                ]
              }
            }
          }
        ]
      }
    }
    ```

    | JSON Path | Type | Presence | Meaning |
    |---|---|---|---|
    | `jobId` | string | Always | Identifier of the job. |
    | `result.outputs` | array of object | When `status` is `succeeded` | One entry per output. |
    | `result.outputs[].destination.content` | object | Embedded `json` outputs | The manifest. See the [Manifest Response Reference][manifest-reference]. |
    | `status` | string | Always | Values: `failed`, `not_started`, `running`, `succeeded`. See [Job Status Response][status-response]. |

5. When `status` is `failed`, read `errorDetails`, fix the request, and submit
   a new job. See [Job Errors][job-errors].

If a request returns `429` or `503`, honor `Retry-After` when present. If it is
absent, retry with increasing delays from 2 to 30 seconds; see
[Retry Guidance][retry].

## Write The Manifest To Your Storage

Once you've created your token, you can make your first API call. This example generates a manifest for a PSD stored at a signed URL:

``` shell
curl --request POST \
  --url https://photoshop-api.adobe.io/v2/generate-manifest \
  --header "Authorization: Bearer $PS_FF_SERVICES_ACCESS_TOKEN" \
  --header "x-api-key: $PS_FF_SERVICES_CLIENT_ID" \
  --header "Content-Type: application/json" \
  --data '{
    "image": {
      "source": { "url": "<SIGNED_GET_URL>" }
    },
    "outputs": [
      {
        "destination": { "url": "<MANIFEST_OUTPUT_URL>" },
        "mediaType": "application/json"
      }
    ]
  }'
```

You'll see a response that contains the job ID and the URL to poll for the job's status:

```json
{
  "jobId": "63c6e812-6cb8-43de-8a60-3681a9ec6feb",
  "statusUrl": "https://photoshop-api.adobe.io/v2/status/63c6e812-6cb8-43de-8a60-3681a9ec6feb"
}
```

Congratulations! You made your first request to the Photoshop API.

## Next Steps

- [Get Job Status][status-response]: the full status response and polling guidance.
- [Output Formats And Options][output-object]: write images and other files.
- [API Reference][api-reference]: every endpoint and field.

[//]: # (Links)
[api-reference]: ../api/photoshop-v2/index.md
[console]: https://developer.adobe.com/
[console-token]: https://developer.adobe.com/developer-console/docs/guides/services/services-add-api-oauth-s2s#generate-token
[destinations]: ../guides/shared-reference/output-formats-and-options.md#choose-a-destination
[embedded]: ../guides/shared-reference/output-formats-and-options.md#embedded-destination
[errors]: ../guides/errors-and-limits/index.md
[job-errors]: ../guides/errors-and-limits/index.md#job-errors
[manifest-reference]: ../guides/photoshop-v2/manifest-response-reference.md
[output-object]: ../guides/shared-reference/output-formats-and-options.md#output-object
[retry]: ../guides/errors-and-limits/index.md#retry-guidance
[s2s]: https://developer.adobe.com/developer-console/docs/guides/services/services-add-api-oauth-s2s/
[signed-urls]: ../guides/shared-reference/input-files-and-storage.md#create-signed-urls
[sources]: ../guides/shared-reference/input-files-and-storage.md#specify-a-source
[status-response]: ../guides/get-job-status/index.md#job-status-response
[url-requirements]: ../guides/shared-reference/input-files-and-storage.md#url-requirements
[console-project]: https://developer.adobe.com/developer-console/docs/guides/projects/projects-empty/
