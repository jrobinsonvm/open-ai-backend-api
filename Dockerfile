# Use a lightweight Python base image
FROM python:3.10.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the application will run on
EXPOSE 5000

# Set the environment variable for the OpenAI API key and organization key
# ENV API_KEY YOUR_API_KEY
# ENV API_SECRET YOUR_ORGANIZATION_KEY

# Run the application
CMD ["python", "openai-api.py"]
