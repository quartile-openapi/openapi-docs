# v2

To standardize endpoints and make them simpler to use, in v2, we made some changes to endpoint input and output contracts. There are several changes between v1 and v2!

- **Changed**: means that the endpoint has changed in some way.
- **Endpoint**: means that the path has changed.
- **Json(In/Out)**: means that the input and output contracts have changed.

!!! Note
    The **~** means that the endpoint is not available in v1. But it is available in v2.

---
**Background processing**

In v2, some endpoints may receive new features; for example, on patch endpoints that end with `/batch` you can send a list of resources to process in the background in a single request, then use the get `/batch/{id}` to check the status of the processing.

Batch processing is an excellent way to reduce the number of requests.

The batch processing is limited to 100 resources per request and the items needs to be unique.

After you send a batch request, you can check the status of the processing using the get `/batch/{id}` endpoint. 

The status code and status can be:

- `206-PENDING`: the batch is in the queue waiting to be processed.
- `206-RUNNING`: the batch is being processed.
- `206-PARTIAL`: the batch has been processed partially.
- `206-FAILED`: the batch has failed to be processed completely.
- `200-SUCCESS`: the batch has been processed successfully.



---

## **OAuth API**

Now the OAuth API v2 has a new endpoint called `/login` used to authenticate the user and return the access and refresh tokens. 
This endpoint is not available in v1.

The `/token` endpoint is deprecated in v2. It is still available in v1 but will be removed in the future.

In v1, the first authentication is necessary to get access and refresh tokens on the Quartile Dev Portal. But now, in v2, you can use the `/login` endpoint to authenticate the user and get the tokens.

The username and password are the same as the ones used to log in on the Quartile Portal.


### **Auth**

Path: `/auth/{version}`

| Methods   | /v1             | /v2        | Changed          | Endpoint         | Json(In/Out)     |
|-----------|-----------------|------------|:----------------:|:----------------:|:----------------:|
| `GET`     | /token          | deprecated | :material-close: | :material-close: | :material-close: |
| `POST`    | /refresh-token  | /refresh   | :material-check: | :material-check: | :material-check: |
| `POST`    | /validate-token | /validate  | :material-check: | :material-check: | :material-close: |
| `POST`    | ~               | /login     | :material-close: | :material-close: | :material-close: |

---

## **Amazon API**

The Amazon API has new changes in v2. You can see the changes in the table below.

All endpoints now add, change or remove only one resource at a time. This means that the input and output contracts are now different from the ones in v1.
You can see the changes in the table below.

---

### **Root**

Path: `/amazon/{version}`


| Methods   | v1         | v2         | Changed          | Endpoint        | Json(In/Out)     |
|-----------|------------|------------|:----------------:|:---------------:|:----------------:|
| `GET`     | /accounts  | /accounts  | :material-close: | :material-close:| :material-close: |

---

### **Pipe**

Path: `/amazon/{version}/pipe`

| Methods   | v1         | v2                       | Changed          | Endpoint         | Json(In/Out)     |
|-----------|------------|--------------------------|:----------------:|:----------------:|:----------------:|
| `GET`     | /campaigns | /campaigns               | :material-check: | :material-close: | :material-check: |
| `GET`     | /adgroup   | /adgroup                 | :material-check: | :material-close: | :material-check: |
| `GET`     | /target    | /target                  | :material-check: | :material-close: | :material-check: |
| `GET`     | /keyword   | /keyword                 | :material-check: | :material-close: | :material-check: |
| `GET`     | /reports   | /reports/{reportId}      | :material-check: | :material-check: | :material-close: |
| `POST`    | /reports   | /reports                 | :material-close: | :material-close: | :material-close: |

---

### **Process**

Path: `/amazon/{version}/process`

| Methods  | v1               | v2                     | Changed          | Endpoint         | Json(In/Out)     |
|----------|------------------|------------------------|:----------------:|:----------------:|:----------------:|
| `GET`    | /masterlist      | /masterlist            | :material-close: | :material-close: | :material-close: |
| `POST`   | /masterlist      | /masterlist            | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /masterlist/{id}       | :material-close: | :material-close: | :material-close: |
| `PUT`    | /masterlist      | /masterlist/{id}       | :material-check: | :material-check: | :material-check: |
| `DELETE` | /masterlist      | /masterlist/{id}       | :material-check: | :material-check: | :material-check: |
| `PATCH`  | ~                | /masterlist/batch      | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /masterlist/batch/{id} | :material-close: | :material-close: | :material-close: |
| `GET`    | /campaignsstatus | /campaigns-status      | :material-check: | :material-check: | :material-close: |
| `POST`   | /campaignsstatus | /campaigns-status      | :material-check: | :material-check: | :material-close: |

---

### **Parameters**

Path: `/amazon/{version}/parameters`

| Methods   | v1         | v2                       | Changed          | Endpoint         | Json(In/Out)     |
|-----------|------------|--------------------------|:----------------:|:----------------:|:----------------:|
| `GET`     | /products  | /products/acos           | :material-check: | :material-check: | :material-close: |
| `POST`    | /products  | /products/acos           | :material-check: | :material-check: | :material-close: |
| `GET`     | ~          | /products/acos/{id}      | :material-close: | :material-close: | :material-close: |
| `PUT`     | /products  | /products/acos/{id}      | :material-check: | :material-check: | :material-check: |
| `DELETE`  | /products  | /products/acos/{id}      | :material-check: | :material-check: | :material-check: |
| `GET`     | ~          | /products/acos/history   | :material-close: | :material-close: | :material-close: |
| `GET`     | /campaigns | /campaigns/acos          | :material-check: | :material-check: | :material-close: |
| `POST`    | /campaigns | /campaigns/acos          | :material-check: | :material-check: | :material-close: |
| `GET`     | ~          | /campaigns/acos/{id}     | :material-close: | :material-close: | :material-close: |
| `PUT`     | /campaigns | /campaigns/acos/{id}     | :material-check: | :material-check: | :material-check: |
| `DELETE`  | /campaigns | /campaigns/acos/{id}     | :material-check: | :material-check: | :material-check: |

---

### **Products**

Path: `/amazon/{version}/products`

| Methods   | v1                | v2                      | Changed          | Endpoint         | Json(In/Out)     |
|-----------|-------------------|-------------------------|:----------------:|:----------------:|:----------------:|
| `GET`     | /tag              | /tags                   | :material-check: | :material-check: | :material-check: |
| `GET`     | ~                 | /tags/{id}              | :material-close: | :material-close: | :material-close: |
| `PUT`     | /tag              | /tags/{id}              | :material-check: | :material-check: | :material-check: |
| `GET`     | /info             | /info                   | :material-check: | :material-close: | :material-check: |
| `POST`    | /info             | /info                   | :material-check: | :material-close: | :material-check: |
| `GET`     | ~                 | /info/{id}              | :material-close: | :material-close: | :material-close: |
| `PUT`     | /info             | /info/{id}              | :material-check: | :material-check: | :material-check: |
| `DELETE`  | /info             | /info/{id}              | :material-check: | :material-check: | :material-check: |
| `GET`     | /inboundinventory | /inbound-inventory      | :material-check: | :material-check: | :material-check: |
| `POST`    | /inboundinventory | /inbound-inventory      | :material-check: | :material-check: | :material-check: |
| `GET`     | ~                 | /inbound-inventory/{id} | :material-close: | :material-close: | :material-close: |
| `PUT`     | /inboundinventory | /inbound-inventory/{id} | :material-check: | :material-check: | :material-check: |
| `DELETE`  | /inboundinventory | /inbound-inventory/{id} | :material-check: | :material-check: | :material-check: |

---

### **Unmanaged**

Path: `/amazon/{version}/unmanaged`

| Methods  | v1               | v2                     | Changed          | Endpoint         | Json(In/Out)     |
|----------|------------------|------------------------|:----------------:|:----------------:|:----------------:|
| `GET`    | ~                | /asins                 | :material-close: | :material-close: | :material-close: |
| `POST`   | ~                | /asins                 | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /asins/{id}            | :material-close: | :material-close: | :material-close: |
| `PUT`    | ~                | /asins/{id}            | :material-close: | :material-close: | :material-close: |
| `DELETE` | ~                | /asins/{id}            | :material-close: | :material-close: | :material-close: |
| `PATCH`  | ~                | /asins/batch           | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /asins/batch/{id}      | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /campaigns             | :material-close: | :material-close: | :material-close: |
| `POST`   | ~                | /campaigns             | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /campaigns/{id}        | :material-close: | :material-close: | :material-close: |
| `PUT`    | ~                | /campaigns/{id}        | :material-close: | :material-close: | :material-close: |
| `DELETE` | ~                | /campaigns/{id}        | :material-close: | :material-close: | :material-close: |
| `PATCH`  | ~                | /campaigns/batch       | :material-close: | :material-close: | :material-close: |
| `GET`    | ~                | /campaigns/batch/{id}  | :material-close: | :material-close: | :material-close: |

---

### **Report**

Path: `/amazon/v2/report`

| Methods   | v1         | v2                           | Changed          | Endpoint         | Json(In/Out)     |
|-----------|------------|------------------------------|:----------------:|:----------------:|:----------------:|
| `POST`    | ~          | /keyword_branded_competitor  | :material-close: | :material-close: | :material-close: |
| `GET`     | ~          | /dowload/{id}                | :material-close: | :material-close: | :material-close: |


---


## **Walmart API**

The Walmart API was released in the Quartile openapi v2.

---


### **Report**

Path: `/walmart/v2/report`

| Methods   | v1         | v2                       | Changed          | Endpoint         | Json(In/Out)     |
|-----------|------------|--------------------------|:----------------:|:----------------:|:----------------:|
| `POST`    | ~          | /adgroup                 | :material-close: | :material-close: | :material-close: |
| `GET`     | ~          | /adgroup                 | :material-close: | :material-close: | :material-close: |
