import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from amqp.rabbit import aio_publish
from s3 import s3_upload


app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Get the bucket name from environment variable
        bucket_name = os.environ['S3_INPUT_BUCKET']

        # Read the file contents
        file_contents = await file.read()

        # Upload the file to S3
        await s3_upload(file_contents, bucket_name, file.filename)

        # Publish a message to the exchange
        message = {
            "type": "upload",
            "bucket": bucket_name,
            "key": file.filename
        }

        host = os.environ['RABBITMQ_HOST']
        user = os.environ['RABBITMQ_USER']
        password = os.environ['RABBITMQ_PASSWORD']
        exchange_name = os.environ['RABBITMQ_EXCHANGE']
        await aio_publish(message, host, user, password, exchange_name, exchange_type='fanout', routing_key='')

        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

