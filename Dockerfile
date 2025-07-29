# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy the entire repository content into the container
# This will create /app/backend/main.py, /app/index.html, etc.
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# ====================================================================
# === KEY CHANGE HERE: UPDATE THE GUNICORN COMMAND ===
#
# Tell gunicorn to look inside the 'backend' folder for the 'main.py' file
# to find the Flask 'app' object. The format is 'folder.filename:app_variable'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "backend.main:app"]
# ====================================================================
