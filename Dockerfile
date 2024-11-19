# Base image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /digitaltwin

# Copy the requirements.txt file into the container at /digitaltwin
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables to non-interactive for automated installs
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    libglu1-mesa \
    libxinerama1 \
    libxxf86vm1 \
    libxft-dev \
    libsm6 \
    libice6 \
    libx11-dev \
    libxext6 \
    libxrender1 \
    blender && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# Copy the Flask app to the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Start the Gunicorn server
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "digitaltwin:create_app()"]
CMD sleep 20 && gunicorn --bind=0.0.0.0:5000 "digitaltwin:create_app()"