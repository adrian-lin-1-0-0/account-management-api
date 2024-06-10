# Account and Password Management API

## Description

This project provides two RESTful HTTP APIs for creating and verifying an account and password.

And uses sqlite3 as the database to store the account information.

- [API Documentation](./doc/api.yaml)



## Endpoints

### 1. Create Account

- **URL**: `/api/create_account`
- **Method**: `POST`
- **Input**: JSON payload with `username` and `password`
- **Output**: JSON payload with `success` and `reason`

Example:

```sh
curl -X POST http://localhost:8000/api/create_account -H "Content-Type: application/json" -d '{"username":"testuser","password":"Password125"}'
```

### 2. Verify Account and Password

- **URL**: `/api/verify_account`
- **Method**: `POST`
- **Input**: JSON payload with `username` and `password`
- **Output**: JSON payload with `success` and `reason`

Example:

```sh
curl -X POST http://localhost:8000/api/verify_account -H "Content-Type: application/json" -d '{"username":"testuser","password":"Password125"}'
```

## Running the Application with Docker

### Prerequisites

- Docker installed

### Steps

1. Pull the Docker image

```sh
docker pull adrianlin0/account-management-api:latest
```

2. Run the Docker container

```sh
docker run -p 8000:8000 adrianlin0/account-management-api:0.0.1
```