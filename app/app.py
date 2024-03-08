import os
import boto3
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure S3 client using environment variables
s3_client = boto3.client(
    's3',
    endpoint_url=os.environ['S3_URL'],
    aws_access_key_id=os.environ['S3_ACCESS_KEY'],
    aws_secret_access_key=os.environ['S3_SECRET_KEY']
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Get the bucket name from environment variable
        bucket_name = os.environ['S3_INPUT_BUCKET']

        # Read the file contents
        file_contents = await file.read()

        # Upload the file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file.filename,
            Body=file_contents
        )

        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)