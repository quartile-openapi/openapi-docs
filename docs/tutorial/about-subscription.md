The 'subscription key' is a unique identifier for your Quartile account.
It is used to authenticate your requests to the Quartile API. This key can be created following the previous step.

The subscription controls your access to our gateway.

A subscription can only be used when activated by Quartile.

## **Using the subscription key**

After activating a subscription through Quartile, you can use it in the request header as a `Subscription-Key` in API v2 and `Ocp-Apim-Subscription-Key` in API v1.


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