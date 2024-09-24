import os
import time
import logging
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import tempfile
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.DEBUG)

upload_folder = tempfile.gettempdir()

pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_CMD', 'tesseract')

app = Flask(__name__)

def textractor(image_path):
  try:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text
  except Exception as e:
    logging.error(f"Error in textractor: {str(e)}")
    return f"Error: {str(e)}"

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
      try:
        image_path = os.path.join(upload_folder, file.filename)
        file.save(image_path)
        extracted_text = textractor(image_path)
        os.remove(image_path)
      except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        extracted_text = f"Error processing image: {str(e)}"
  return render_template("index.html", extracted_text=extracted_text)

def delete_old():
  current_time = time.time()
  for filename in os.listdir(upload_folder):
    file_path = os.path.join(upload_folder, filename)
    if os.path.isfile(file_path):
      file_age = current_time - os.path.getctime(file_path)
      if file_age > 10:
        try:
          os.remove(file_path)
          print(f"{file_path} just got deleted XD")
        except PermissionError:
          print(f"Could not delete {file_path}: File is in use")
        except Exception as e:
          print(f"Error deleting {file_path}: {str(e)}")

if __name__ == "__main__":
  print(f"Tesseract command: {pytesseract.pytesseract.tesseract_cmd}")
  print(f"TESSDATA_PREFIX: {os.environ.get('TESSDATA_PREFIX')}")
  scheduler = BackgroundScheduler()
  scheduler.add_job(func=delete_old, trigger="interval", minutes=.1)
  scheduler.start()
  
  try:
    app.run(debug=True)
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
