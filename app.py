from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import os
import time
import platform
import tempfile
from apscheduler.schedulers.background import BackgroundScheduler

upload_folder = tempfile.gettempdir()

if platform.system() == "Windows":
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
  pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)

def textractor(image_path):
  image = Image.open(image_path)
  text = pytesseract.image_to_string(image)
  return text

@app.route("/", methods=["GET", "POST"])
def main():
  extracted_text = None
  if request.method == "POST":
    if "image" not in request.files:
      return redirect(request.url)
    file = request.files["image"]
    if file.filename == "":
      return redirect(request.url)
    if file:
      image_path = os.path.join(upload_folder, file.filename)
      file.save(image_path)
      extracted_text = textractor(image_path)
      os.remove(image_path)
  return render_template("index.html", extracted_text=extracted_text)

def delete_old():
  current_time = time.time()
  for filename in os.listdir(upload_folder):
    file_path = os.path.join(upload_folder, filename)
    if os.path.isfile(file_path):
      file_age = current_time - os.path.getctime(file_path)
      if file_age > 10:
        os.remove(file_path)
        print(f"{file_path} just got deleted XD")

if __name__ == "__main__":
  scheduler = BackgroundScheduler()
  scheduler.add_job(func=delete_old, trigger="interval", minutes=.1)
  scheduler.start()
  
  try:
    app.run(debug=True)
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()