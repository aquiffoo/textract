#!/bin/bash
apt-get update && apt-get install -y tesseract-ocr
pip install -r requirements.txt
tesseract --version
python --version