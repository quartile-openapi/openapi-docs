## Token lifetimes

The following token lifetimes are provided to further your knowledge. They can help you when you develop and debug apps. Note that your apps should not be written to expect any of these lifetimes to remain constant. They can and will change if an anomaly is identified.


| Token | Lifetime | Description |
| ----------------------- | ------------------------------- | ------------ |
| Access tokens | One hour | ID tokens are typically valid for an hour. Your web app can use this lifetime to maintain its own sessions with users (recommended).You cannot currently choose a different session duration. If your app needs to get a new access token, you can generate a new set of tokens using refresh token. |
| Refresh tokens | Up to 14 days | A single refresh token is valid for a maximum of 14 days. However, a refresh token may become invalid at any time for any number of reasons (For example: You generated multiple sets of tokens using the same token). Your app should continue to try to use a refresh token until the request fails, or until your app replaces the refresh token with a new one.  A refresh token also can become invalid if 90 days has passed since the user last entered credentials. |

## Working

We are working to improve the way to create tokens (login), if you lose both accesses (Access Token and refresh token) you can login again using (Email and Password Quartile)