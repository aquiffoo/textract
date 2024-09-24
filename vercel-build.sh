#!/bin/bash

apt-get update

apt-get install -y tesseract-ocr libtesseract-dev

which tesseract
tesseract --version

if [ ! -f /usr/local/bin/tesseract ]; then
    ln -s "$(which tesseract)" /usr/local/bin/tesseract
fi

pip install -r requirements.txt

mkdir -p /var/task/tessdata

cp -r /usr/share/tesseract-ocr/4.00/tessdata/* /var/task/tessdata/ || cp -r /usr/share/tesseract-ocr/tessdata/* /var/task/tessdata/

export TESSDATA_PREFIX=/var/task/tessdata
echo "TESSDATA_PREFIX set to $TESSDATA_PREFIX"
