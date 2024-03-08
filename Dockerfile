FROM python:3.11-slim

# Set the working directory in the container

WORKDIR /app

COPY ./requirements.txt .

# Install the dependencies

RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory

COPY ./app .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
