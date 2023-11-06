# Use a base Python image
FROM python:3.11.6 as python

# Python build stage
FROM python as python-build-stage

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create Python Dependency and Sub-Dependency Wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt

# Python 'run' stage
FROM python as python-run-stage

# Set the working directory
WORKDIR /app

# Copy the wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /usr/src/app/wheels

# Copy your application code
COPY . /app

# Install your project's requirements

RUN pip install --no-cache-dir -r requirements.txt
