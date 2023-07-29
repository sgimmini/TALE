# Docker Setup Documentation
Docker Engine version: `24.0.2`
Docker Compose version: `v2.19.1`

## Organization
`Dockerfile` to build the image for the application is located in the root directory of the project, as well as the `docker-compose.yml` file is located in the root directory of the project. 
The `docker-compose.yml` file is used to build the image and run the container.

## Build
To build the image, run the following command in the root directory of the project:
```
docker compose build
```

## Run
To run the container, run the following command in the root directory of the project:
```
docker compose up -d
```

## Run and Build
To build the image and run the container, run the following command in the root directory of the project:
```
docker compose up -d --build
```

## Stop
To stop the container, run the following command in the root directory of the project:
```
docker compose down
```
This will stop the container and remove it.

## Access
To access the container, run the following command in the root directory of the project:
```
docker exec -it <container_name> /bin/bash
```
This will open a bash shell inside the container.

## Send Requests
To send requests to the container, it is the easiest to use postman, and the vscode postman extension. 
For testing purposes, there is a simple calculation implemented which can be triggered by sending the following request to the container:
1. set header: `Content-Type: application/json`
2. set body: `{"data1": 1, "data2": 2, }`
3. send request to: `http://localhost:8000/calculate_sum`