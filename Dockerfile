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

# === THE FINAL, CRITICAL FIX IS ON THIS LINE ===
# We are telling Gunicorn to wait up to 310 seconds for a request to complete,
# which is longer than the 300-second timeout in our requests call.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "360", "main:app"]
