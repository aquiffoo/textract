#!/bin/bash

apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng

pip install -r requirements.txt

mkdir -p /var/task/tessdata
cp /usr/share/tesseract-ocr/4.00/tessdata/* /var/task/tessdata/ || cp /usr/share/tesseract-ocr/tessdata/* /var/task/tessdata/

tesseract --version

python --version