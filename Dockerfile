FROM python:3.11

# Update pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install --upgrade build

# Copy the project
COPY . /app

# Set the working directory
WORKDIR /app

ENTRYPOINT python -m build
