FROM python:3.11.6-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        postgresql \
        libpq-dev \
        gcc \
        python3-dev \
        musl-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (if necessary)
EXPOSE 8000

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]