# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install --no-cache-dir Flask==2.1.2

# Install Flask-RESTful
RUN pip install --no-cache-dir Flask-RESTful==0.3.9

# Install Flask-SQLAlchemy
RUN pip install --no-cache-dir Flask-SQLAlchemy==3.0.1

# Install Celery
RUN pip install --no-cache-dir celery==5.2.3

# Install SQLAlchemy
RUN pip install --no-cache-dir SQLAlchemy==1.4.31

# Expose port 5000 to the outside world
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "queues.py"]
