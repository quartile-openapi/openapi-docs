The OAuth2 system is premised on having a token expiration process.

This can cause problems when you need to call a service asynchronously many times. In this period of time the access token may expire.

This tutorial provides a way to deal with this problem.

---

## **Solving**

- **Database** to save the tokens.
- **Worker** to update the refresh token when there is 1 hour left to expire.
- **Microservice** to provide the most up-to-date token.

---

## **Using Python and PostgreSQL**

This example uses Python as the programming language and PostgreSQL as the database.

---

## **GitHub - Code**

This GitHub folder has all the files mentioned in the tutorial.

[GitHub :material-github:](https://github.com/quartile-openapi/openapi-docs/tree/main/docs/tutorial/python/tokens/){ .md-button }

---

## **Install Dependencies**

The dependencies used in this tutorial are:

* **pysqlx-engine**: SQL Engine
* **httpx**: HTTP Client


<div class="termy">

```console
$ pip install httpx pysqlx-engine
Requirement already satisfied: httpx in ./.pyenv/versions/3.10.1/lib/python3.10/site-packages (1.4.36)
Collecting pysqlx-engine
  Downloading pysqlx_engine-2.9.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 25.9 MB/s eta
...
...

```
</div>

## **File Structure**

The file structure is as follows:

``` { .sh .no-copy }
.
├─ database.py
├─ schema.py
├─ consumer.py
└─ worker.py
```

---

## **Code**


### **database.py**

This file contains the database connection and the class that represents the table.

The `TokenDB` class will be used to save the tokens in the database.


```Python title="database.py"
{!./tutorial/python/tokens/database.py!}
```

---

### **schema.py**

This file contains the models that represent the tokens.

The `AuthToken` class will be used to parse the response from the Quartile API.

```Python title="schema.py"
{!./tutorial/python/tokens/schema.py!}
```

---

### **consumer.py**

This file contains the code that will consume the token, and you can see that the token is returned when the `updating` field is `False`!

This status is changed by `worker.py` when the token is updated.

```Python title="consumer.py"
{!./tutorial/python/tokens/consumer.py!}
```

---

### **worker.py**

The `worker.py` is responsible for updating the token when it is about to expire.

The access token expires in 12 hours, so the worker will update the token when there is 1 hour left to expire.

For example, you can put on the worker a scheduler to run every 30 minutes. Or you can run it in a separate process.

Some cloud companies provide simple ways to run this kind of routine using a timer trigger, for example:

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Google Cloud Functions](https://cloud.google.com/functions)
- [Azure Functions](https://azure.microsoft.com/en-us/services/functions/)

```Python title="worker.py"
{!./tutorial/python/tokens/worker.py!}
```

---

## **Run the code**


=== "**Terminal 1: :fontawesome-brands-python: worker.py**"

    <div class="termy">

    ```console
    $ python worker.py

    waiting for token update...
    ...

    ```
    </div>

=== "**Terminal 2: :fontawesome-brands-python: consumer.py**"

    <div class="termy">

    ```console
    $ python consumer.py

    getting token...
    ...

    ```
    </div>