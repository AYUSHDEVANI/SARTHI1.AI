# Use the official Rasa image as the base
FROM rasa/rasa:3.0.0

# Set the working directory for Rasa
WORKDIR /app

# Copy Rasa project files into the container
COPY ./rasa /app/rasa

# Install additional Python dependencies for your Flask app
COPY ./app /app/app
RUN pip install -r /app/app/requirements.txt

# Expose necessary ports
EXPOSE 5000  
EXPOSE 5005  

# Run Rasa and Flask app in the container
CMD ["sh", "-c", "rasa run -m /app/rasa/models --enable-api --cors '*' & python /app/app/app.py"]
