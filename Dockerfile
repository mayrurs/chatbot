# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8501

# Set environment variable to avoid Streamlit's telemetry message
ENV STREAMLIT_TELEMETRY_OPTOUT=true

# Run the application
CMD ["streamlit", "run", "chatbot.py"]

