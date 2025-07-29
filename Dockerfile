# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This copies main.py, static/, and templates/ into /app
COPY . .

EXPOSE 8080

# This command is now correct because main.py is in the root of /app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
