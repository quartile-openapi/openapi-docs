
### **Subscriber and Authorization**
Access Control (Subscriber) and Authorization (OAuth2), by default, all the requests to our API require a subscriber key and authorization token.

You will learn how to get a subscriber key and authorization token in the following steps.

### **Subscriber Key**
The subscriber is used to:

- Access control on the API
    - Control requests,
    - Reports,
    - Limits and access products.

!!! Note "Subscriber Key"
    The subscriber key is required to access our API.

    P.S.: A subscriber key is 32-character alphanumeric text that contains a value that uniquely identifies a subscriber in our API.

    The Subscriber Key is sent in the request header.

    For example:

    ```http
    GET /amazon/v2/ HTTP/1.1
    Host: api.quartile.com
    Content-Type: application/json
    Authorization: Bearer eyJ0eXA...
    Subscription-Key: <your_subscription_key>  
    ```

### **Authorization (OAuth2)**
The authorization token is used to validate your identity in Quartile LLC, this token is required to access our API.

!!! Note "Authorization Token"
    The authorization token is required to access our API.
    
    P.S: An authorization code is an alphanumeric password that authorizes your user to search, change, delete, or enter information into a security-protected API.

    The Authorization Token is sent in the request header.

    For example:

    ```http
    GET /amazon/v2/ HTTP/1.1
    Host: api.quartile.com
    Content-Type: application/json
    Authorization: Bearer <your_authorization_token>
    Subscription-Key: xyxysc98eud840afecc241f7ru3jnxyz
    ```
