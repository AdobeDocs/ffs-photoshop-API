title: Authentication
description: Page for Authentication
contributors:
  - https://github.com/khound
---

# Authentication

Server-to-server authentication credentials let your application's server generate access tokens and make API calls on behalf of your application.

For your application to generate an access token, an end user does not need to sign in or provide consent to your application. Instead, your application can use its credentials (client ID and secrets) to authenticate itself and generate access tokens. Your application can then use these to call Adobe APIs and services on its behalf.

This is sometimes referred to as "two-legged OAuth".

## Access tokens

Each access token is valid for 24 hours. To adhere to OAuth best practices, you should generate a new token every 23 hours.

Generate access tokens programmatically by sending a POST request:

```bash
curl -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=openid,AdobeID,firefly_api,ff_apis'
```

The required parameters are:

- `client_id`: The Client ID.
- `client_secret`: The Client secret.
- `scope`: The scopes are `openid`, `AdobeID`, `firefly_api`, `ff_apis`.

Automate your token generation by calling the IMS endpoint above using standard OAuth2 libraries. Using industry-standard libraries is the quickest and most secure way of integrating with OAuth.

Be diligent when choosing the OAuth 2.0 library that works best for your application. Your teams' projects likely leverage OAuth libraries already to connect with other APIs. It's recommended to use these libraries to automatically generate tokens when they expire.

The token endpoint also returns an expiry date, and the token itself (when decoded) contains the expiry time.

Once you’ve created your token, you can follow the steps below to make your first API call.
   - Open your terminal and paste the code below.
   - Replace the variables "YOUR_ACCESS_TOKEN" with the token you generated on Adobe I/O Console.
   - Replace <YOUR_CLIENT_ID>. You can find this on the same page you generated your token on.
   - Once all variables have been replaced you can run the command.

``` shell
curl --request GET \
  --url https://image.adobe.io/pie/psdService/hello \
  --header "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  --header "x-api-key: <YOUR_CLIENT_ID>"
```

If you are using Windows machine don't use the backslash for the curl commands. e.g
``` shell
curl --request GET --url https://image.adobe.io/pie/psdService/hello --header "Authorization: Bearer <YOUR_ACCESS_TOKEN>" --header "x-api-key: <YOUR_CLIENT_ID>"
```
Congratulations! You just made your first request to the Photoshop API.