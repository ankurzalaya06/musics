# Use Python 3.8.10 base image
FROM python:3.8.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create directory for the Django project
RUN mkdir /music_service

# Set working directory
WORKDIR /music_service

# Copy all project files to the Docker image
COPY . /music_service/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# CMD has to be a single instruction, so combine the commands
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
