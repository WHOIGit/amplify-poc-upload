# File Upload Microservice

This is a microservice application that allows uploading files to an S3 compatible storage and publishing messages to a RabbitMQ exchange.

## Prerequisites

Before running the application, make sure you have the following:

- Docker installed and running on your machine
- RabbitMQ server running and accessible
- S3 compatible storage (e.g., AWS S3, MinIO) configured and accessible

## Configuration

The application requires the following environment variables to be set:

```
RABBITMQ_HOST=<rabbitmq-host>
RABBITMQ_USER=<rabbitmq-user>
RABBITMQ_PASSWORD=<rabbitmq-password>
RABBITMQ_EXCHANGE=<rabbitmq-exchange>
S3_URL=<s3-url>
S3_ACCESS_KEY=<s3-access-key>
S3_SECRET_KEY=<s3-secret-key>
S3_INPUT_BUCKET=<s3-input-bucket>
```

Replace `<rabbitmq-host>`, `<rabbitmq-user>`, `<rabbitmq-password>`, `<rabbitmq-exchange>`, `<s3-url>`, `<s3-access-key>`, `<s3-secret-key>`, and `<s3-input-bucket>` with your actual values.

## Usage

1. Build and run the Docker container:

```
docker build -t file-upload-microservice .
docker run -p 8000:8000 \
 -e RABBITMQ_HOST=<rabbitmq-host> \
 -e RABBITMQ_USER=<rabbitmq-user> \
 -e RABBITMQ_PASSWORD=<rabbitmq-password> \
 -e RABBITMQ_EXCHANGE=<rabbitmq-exchange> \
 -e S3_URL=<s3-url> \
 -e S3_ACCESS_KEY=<s3-access-key> \
 -e S3_SECRET_KEY=<s3-secret-key> \
 -e S3_INPUT_BUCKET=<s3-input-bucket> \
 file-upload-microservice
```

Alternately, use `docker compose` and a `.env` file (or equivalent means) to configure the container.

2. Upload a file using the `/upload` endpoint:

```
curl -X POST -F "file=@/path/to/my/file" http://localhost:8000/upload
```

Upon successful upload, the file will be stored in the specified S3 bucket, and a message will be published to the configured RabbitMQ exchange.

## File Structure

- `app.py`: The main FastAPI application file that defines the `/upload` endpoint.
- `s3.py`: Contains the `s3_upload` function for uploading files to S3 compatible storage.
