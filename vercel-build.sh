#!/bin/bash

apt-get update

apt-get install -y tesseract-ocr
apt-get install -y libtesseract-dev

pip install -r requirements.txt

mkdir -p /var/task/tessdata

cp -r /usr/share/tesseract-ocr/4.00/tessdata/* /var/task/tessdata/ || cp -r /usr/share/tesseract-ocr/tessdata/* /var/task/tessdata/

which tesseract
tesseract --version

python --version

export TESSDATA_PREFIX=/var/task/tessdata