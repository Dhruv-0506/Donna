# Dockerfile (Now located at the repository root)

# Step 1: Use an official lightweight Python image.
FROM python:3.10-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Copy the requirements file from the root into the container.
COPY requirements.txt .

# Step 4: Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your application code from the 'backend' folder into the container.
# This path is now relative to the Dockerfile's new location.
COPY backend/main.py .

# Step 6: Expose port 8080.
EXPOSE 8080

# Step 7: Define the command to run your application using gunicorn.
# The target is still 'main:app' because we copied main.py into the root of /app.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
