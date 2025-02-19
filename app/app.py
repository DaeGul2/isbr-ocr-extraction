from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import os
import pandas as pd
import re
import json
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 최대 파일 크기 제한

# CLOVA OCR 설정
CLOVA_OCR_URL = "https://2khcjstlni.apigw.ntruss.com/custom/v1/38372/c0900a14255a3a2be14c0ee063c3c5536a71f856761a130c6e6f30c9ec93c899/general"
CLOVA_SECRET_KEY = "a0h2R1p3TFJOWUxqWXl3VGJLcFVsc3F1UmpJYkdtalU="

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            socketio.emit('file_uploaded', {'file_path': file_path}, namespace='/progress')
            return redirect(request.url)
    return render_template('index.html')

def extract_text_from_image(image_path):
    headers = {"X-OCR-SECRET": CLOVA_SECRET_KEY}
    payload = {
        "version": "V2",
        "requestId": str(int(time.time() * 1000)),
        "timestamp": int(time.time() * 1000),
        "images": [{"format": "jpg", "name": "ocr_image"}]
    }
    if os.path.getsize(image_path) > 10 * 1024 * 1024:
        return "File size exceeds the limit"
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        data = {"message": json.dumps(payload)}
        response = requests.post(CLOVA_OCR_URL, headers=headers, data=data, files=files, timeout=15)
        result = response.json()
        extracted_text = [field["inferText"] for image in result.get("images", []) for field in image.get("fields", [])]
        return " ".join(extracted_text)

def handle_ocr_process(file_path):
    text = extract_text_from_image(file_path)
    socketio.emit('ocr_done', {'text': text}, namespace='/progress')

@socketio.on('start_ocr', namespace='/progress')
def start_ocr(message):
    file_path = message['file_path']
    handle_ocr_process(file_path)

if __name__ == '__main__':
    socketio.run(app, debug=True)
