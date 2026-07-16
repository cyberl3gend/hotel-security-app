# ⚠️ VULNERABLE VERSION — full Ubuntu base image
FROM ubuntu:22.04

# Set working directory inside container
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the app
CMD ["python3", "app.py"]
