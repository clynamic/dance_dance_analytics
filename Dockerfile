# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]
