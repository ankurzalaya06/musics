# Use Python 3.8.10 base image
FROM python:3.8.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create directory for the Django project
RUN mkdir /music_service

# Set working directory
WORKDIR /music_service

# Copy all project files to the Docker image
ADD . /music_service/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Make migrations
CMD ["python", "manage.py", "makemigrations"]

# Migrate the database
CMD ["python", "manage.py", "migrate"]