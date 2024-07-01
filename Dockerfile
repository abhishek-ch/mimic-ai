# Use the open-webui image as the base image
FROM ghcr.io/open-webui/open-webui:main


RUN apt-get update
# Install DuckDB Python package
RUN pip3 install -r requirements.txt


# Set the working directory
WORKDIR /app

# Copy your application code to the container
# Expose the port
EXPOSE 8080

# Start the open-webui service
CMD ["sh", "-c", "cd /app/backend && ./start.sh"]

# Restart always
LABEL restart=always