# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy app code
COPY . .
COPY notekeeper/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Build chatbot model during build, so final image includes model + pkl files
RUN python notekeeper/train_model.py

# Environment variables
ENV FLASK_APP=notekeeper:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Expose port
EXPOSE 8080

# Start Flask directly
CMD ["flask", "run"]
