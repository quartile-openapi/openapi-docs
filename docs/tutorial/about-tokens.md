## **Token lifetimes**

The following token lifetimes are provided to further your knowledge. They can help you when you develop and debug apps. Note that your apps should not be written to expect any of these lifetimes to remain constant. They can and will change if an anomaly is identified.


| Token | Lifetime | Description |
| ----------------------- | ------------------------------- | ------------ |
| Access tokens | Up to 12 hours | Access token are typically valid for 12 hours. Your web app can use this lifetime to maintain its own sessions with users (recommended).You cannot currently choose a different session duration. If your app needs to get a new access token, you can generate a new set of tokens using refresh token. |
| Refresh tokens | Up to 14 days | A single refresh token is valid for a maximum of 14 days. However, a refresh token may become invalid at any time for any number of reasons (For example: You generated multiple sets of tokens using the same token). Your app should continue to try to use a refresh token until the request fails, or until your app replaces the refresh token with a new one.|



### **Using the access token**
 
The access token is passed in the request's Authorization **header**, as a Bearer token.

### **Example**

Change the `<subscription_key>` and `<access_token>` to your own values.

=== "v2"
    ```http
    GET /amazon/v2/accounts HTTP/1.1
    Host: api.quartile.com
    Subscription-Key: <subscription_key>
    Authorization: Bearer <access_token>
    ```

=== "v1"
    ```http
    GET /amazon/v1/accounts HTTP/1.1
    Host: api.quartile.com
    Ocp-Apim-Subscription-Key: <subscription_key>
    Authorization: Bearer <access_token>
    ```