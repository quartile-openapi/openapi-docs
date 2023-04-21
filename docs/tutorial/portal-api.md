# Quartile Developer Portal
Quartile Dev Portal has a simple option for you to make requests in our API and export code examples in Java, C#, Python, PHP etc.

Log in to the developer portal and go to the API page..

---

## **Access API**

<img src="./img/portal_api_00.png" alt="Access API">

---

## **Select an API**

<img src="./img/portal_api_01.png" alt="Select an API">

---

## **Select an Endpoint**

<img src="./img/portal_api_02.png" alt="Select an Enpoint">

---

## **See requirements for request**

All request parameters have a predescription of what that field is.

<img src="./img/portal_api_03.png" alt="See requirements for request">

---

## **What will return?**

Before making a request you can see what the endpoint should return.
Scroll down to the response part, you can see what the status and return type of this endpoint is.


### **Successfull response**

<img src="./img/portal_api_04.png" alt="Successfull response">

### **Unauthorized**

<img src="./img/portal_api_05.png" alt="Unauthorized">

### **Unprocessable Entity**

<img src="./img/portal_api_06.png" alt="Unprocessable Entity">

---
## **Try it**

Make the request by clicking on **Try it**

### **Click on the button _Try it_**

<img src="./img/portal_api_07.png" alt="button try it">

### **Select authorization_code**

If it is the first access, a window will open for you to login to generate an access token, 
after login the dev portal will automatically set an access token in your requests.

### **Generate token automatically**

<img src="./img/portal_api_08.png" alt="Generate token automatically">

### **After generate token**

The access token will be automatically set in the request header.

<img src="./img/portal_api_09.png" alt="After generate token">


### **Select subscription key**

The subscription key is automatically set if you have a Quartile-enabled key for your access.

<img src="./img/portal_api_10.png" alt="After generate token">


### **Set the profileId**

Case you don't have the profileId, you can get using the endpoint **/amazon/{version}/accounts**.

<img src="./img/portal_api_11.png" alt="After generate token">


### **Send request**

When you click on the button **Send**, the request will be sent and the response will be displayed.

<img src="./img/portal_api_12.png" alt="After generate token">

### **See the response.**

The response will be displayed in the response part.

<img src="./img/portal_api_13.png" alt="After generate token">