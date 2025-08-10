# Use official Python 3.10 base image
FROM python:3.10.14-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libmysqlclient-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entire app code into the container
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "-p", "0.0.0.0:8000"]
