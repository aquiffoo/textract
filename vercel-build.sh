#!/bin/bash
apt-get update

apt-get install -y tesseract-ocr libtesseract-dev

which tesseract
tesseract --version

pip install -r requirements.txt

mkdir -p /var/task/tessdata

cp -r /usr/share/tesseract-ocr/4.00/tessdata/* /var/task/tessdata/ || cp -r /usr/share/tesseract-ocr/tessdata/* /var/task/tessdata/

echo "TESSDATA_PREFIX is set to $TESSDATA_PREFIX"
