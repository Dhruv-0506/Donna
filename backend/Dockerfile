
# backend/Dockerfile

# Step 1: Use an official lightweight Python image as a parent image.
# python:3.10-slim is a good balance of size and functionality.
FROM python:3.10-slim

# Step 2: Set the working directory inside the container.
# All subsequent commands will run from this directory.
WORKDIR /app

# Step 3: Copy the requirements file into the container.
COPY requirements.txt .

# Step 4: Install the Python dependencies listed in the requirements file.
# --no-cache-dir reduces the size of the final image.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your application code (main.py) into the container.
COPY main.py .

# Step 6: Inform Docker that the container listens on port 8080 at runtime.
# This is a standard port for serverless platforms.
EXPOSE 8080

# Step 7: Define the command to run your application using gunicorn.
# This is the command that starts your server when the container launches.
# It binds the server to 0.0.0.0:8080, making it accessible from outside the container.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
