# 1. Choose the base operating system (A lightweight version of Linux with Python 3.9)
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file into the container
COPY requirements.txt .

# 4. Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your AI models and API code into the container
COPY models/ ./models/
COPY api.py .

# 6. Open port 8000 for the outside world to communicate with the container
EXPOSE 8000

# 7. The command to start the FastAPI server when the container turns on
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]