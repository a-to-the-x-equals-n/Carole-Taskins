# OS
FROM ubuntu:22.04

# Set the working directory
WORKDIR /app/server

# Copy the app folder contents to the working directory
COPY server/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3 python3-pip \

RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run main.py when the container launches
CMD ["python3", "app.py"]
