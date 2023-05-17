# Updating tokens

Tokens are used to authenticate users and services.
In this folder, you can find the code to generate and verify tokens.

The `consumer.py` is an example of how to get the access token from the database.
The `worker.py` is an example of how to update the token in the database.


### PostgreSQL

The tokens are stored in the database.

You can use the command below to create the docker container with the database.

```bash
docker run --name postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=quartile \
    -p 5432:5432 \
    -d postgres
```

