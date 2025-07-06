# use an official Python 3.10 image from docker Hub
FROM python:3.13-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy your application code 
COPY . /app 

# Install the dependencies
RUN pip install -r requirements.txt 

# Expose the port FastAPI will run on
EXPOSE 5000 

# Command to run FastAPI app
CMD ["python3","app.py"]

