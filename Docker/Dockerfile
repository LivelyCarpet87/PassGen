# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask gunicorn

# Copy app files
COPY ./app /app/

# Expose port
EXPOSE 8080

# Use Gunicorn to serve the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "4", "--threads", "2"]
