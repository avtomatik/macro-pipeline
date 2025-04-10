# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Upgrade pip and install dependencies into the virtual environment
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt --no-cache-dir

# Set the virtual environment's bin directory to the PATH
ENV PATH="/app/venv/bin:$PATH"

# Run the dataset script when container launches
CMD [ "python3", "src/dataset.py" ]
