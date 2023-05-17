# v2 - Authorization

OAuth2 JWT authorization is a secure way to transfer personal data and validate identity.

In this new version, you can use the `/login` endpoint to log in and generate a new set of tokens.

!!! warning
    The access token and authorization token are the same thing. 

* **Authorization Token:** Use this token to make requests to our API! Send this token in the request header. The token expires 720 minutes (12 hours) after it is created.

* **Refresh Token:** Use this token to request a new set of tokens. This token expires 14 days after being created.

!!! warning "Warning :material-refresh: Refresh token"
    When the access token expires and you request a new set of tokens,
    the refresh token will also be updated! **So always save the last refresh token**,
    so you won't have any problems. The refresh token may expire or be disabled when
    you request a new set of tokens!

    You can learn how to deal with this "problem" in the session: [Updating tokens](/tutorial/updating-tokens.html)
---

!!! Danger "Deprecated :material-alert-circle:"
    The old version(v1) of the authorization is still available, but it will be deprecated in the future. 
    We recommend that you use the new version(v2) of the authorization.

## **Login**

After creating an account in the [Developer Portal](https://developer.quartile.com/signin), you can use the login endpoint to generate a new set of tokens.

!!! info "Info :material-information-outline:"
    The login endpoint is available from the [OAuth API](https://developer.quartile.com/api-details#api=auth-v2) on the Developer Portal.

Make a `POST` request to the login endpoint. Change the `<your@email.com>` and `<your_password>` with your email and password.
Remember to use the same email and password you used to log in to your account in the Developer Portal.


```http
POST /auth/v2/login HTTP/1.1
Host: api.quartile.com
Content-Type: application/json
Subscription-Key: <subscription_key>

{
    "username": "<your@email.com>",
    "password": "<your_password>"
}

```

---

#### **Response**

If you have logged in correctly, a set of tokens will be generated.

```JSON
{!../docs/files/token.json!}
```

---

### **Endpoints** 

You can make API calls and request new tokens through the refresh endpoint with the generated tokens. 

Access: [OAuth API](https://developer.quartile.com/api-details#api=auth-v2) 


| **Method** | **Type**   | **URL**                            | **Description** |
| :--------- |:---------- | :--------------------------------- | :-------------- |
| `POST`     | *Login*    | :material-check: /auth/v2/login    | The login endpoint is used to generate a new set of tokens. You can use the generated tokens to make API calls. |
| `POST`     | *Refresh*  | :material-check: /auth/v2/refresh  | You need to enter the update token. If you do not have this data, make a new login using the `/login` endpoint. **Always save the last refresh token to use next time.** |
| `POST`     | *Validade* | :material-check: /auth/v2/validate | You can verify that the authorization token is valid. |