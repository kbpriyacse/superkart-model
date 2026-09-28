
# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into the container
COPY . .

# Flask/Gunicorn will run on port 5000
EXPOSE 5000

# Start the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:superkart_api"]
