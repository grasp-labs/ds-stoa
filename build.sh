#!/bin/bash

# This script will build the package using docker

# Get the directory of the script
script_dir=$(dirname "$0")
echo "Working directory: $script_dir"

# Save the original directory
orig_dir=$(pwd)

# Change to the directory containing the script
cd $script_dir

echo "Building Docker image"
docker build -t python-package-image .

echo "Building package"
docker run --name python-package-container python-package-image

echo "Copying package dist"
docker cp python-package-container:/app/dist .
docker cp python-package-container:/app/src .

echo "Removing package container"
docker rm python-package-container

# Change back to the original directory
cd $orig_dir
