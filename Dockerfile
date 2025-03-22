# Use a lightweight Python base image
FROM python:3.9.6-alpine3.14 AS build

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Update package index and install build dependencies
RUN apk update \
    && apk add --no-cache gcc libffi-dev musl-dev ffmpeg \
    # Add the community repository for aria2c
    && apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community aria2 \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Use a smaller base image for the final build
FROM python:3.9.6-alpine3.14

# Set the working directory
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /app .

# Command to run both Gunicorn and the Python script
CMD ["sh", "-c", "gunicorn app:app & python3 main.py"]
