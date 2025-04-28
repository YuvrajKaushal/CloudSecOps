# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask application port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]

COPY demo_threats.sh /app/demo_threats.sh
RUN chmod +x /app/demo_threats.sh
