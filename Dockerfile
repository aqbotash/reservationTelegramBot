FROM python:3.11

# Set environment variables
ENV BOT_TOKEN="6258824392:AAEE_I40M8E908SUNoHttH-pLM3E6Kh6Qf4"
ENV GOOGLE_SHEETS_CREDENTIALS_FILE=/app/service_account.json

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make sure you have your Google Sheets credentials file (your_google_sheets_credentials.json) in the same directory as your Dockerfile

# Run your Python script when the container launches
CMD ["python", "bot.py"]