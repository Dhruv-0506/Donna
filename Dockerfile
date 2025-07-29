# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This will copy main.py, and the static/ and templates/ folders
COPY . .

EXPOSE 8080

# The command to run the application.
# It now references 'main:app' directly because main.py is in the root.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
