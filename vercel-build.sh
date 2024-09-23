#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y tesseract-ocr

# Install Python dependencies
pip install -r requirements.txt

# Copy Tesseract data to the function's root
mkdir -p /var/task/tessdata
cp /usr/share/tesseract-ocr/4.00/tessdata/* /var/task/tessdata/