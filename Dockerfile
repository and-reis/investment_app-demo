# Official Python base image
FROM python:3.12-slim

# Add the curl command to the environment
RUN apt-get update && apt-get install -y curl netcat-openbsd

# Set the working directory in the container
WORKDIR /home

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the dependency file
COPY requirements.txt ./requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY backend .

# Expose the default FastAPI port
EXPOSE 8000

# Add an entrypoint script
ENTRYPOINT ["sh", "/home/entrypoint.sh"]

# Default command to start FastAPI
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["sh", "-c", "export PYTHONPATH=$(pwd) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
