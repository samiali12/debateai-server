# python base image
FROM python:3.11-slim AS base 

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory inside container
WORKDIR /app 

# Copy requirements.txt to contain 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

# Copy all project file into container  dire 
COPY . .

# Run container on port 
EXPOSE 8000 

# Run these commands when container start 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]