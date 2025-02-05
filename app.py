from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

@app.route('/')
def home():
    return "API Çalışıyor!"

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def calculate_fill_percentage(processed_image):
    total_pixels = processed_image.size
    filled_pixels = cv2.countNonZero(processed_image)
    return (filled_pixels / total_pixels) * 100

@app.route('/calculate', methods=['POST'])
def calculate_volume():
    try:
        volume = float(request.form['containerVolume'])
        image_file = request.files['containerImage']
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        processed_image = process_image(image)
        fill_percentage = calculate_fill_percentage(processed_image)
        filled_volume = (fill_percentage / 100) * volume

        return jsonify({
            'fill_percentage': round(fill_percentage, 2),
            'filled_volume': round(filled_volume, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
