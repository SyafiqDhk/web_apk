from flask import Flask, render_template, request, send_file, jsonify
import barcode
from barcode.writer import ImageWriter
import io
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    item_name = request.form['item_name']

    # Generate barcode
    code128 = barcode.get_barcode_class('code128')
    code = code128(item_name, writer=ImageWriter())

    # Create an in-memory buffer to store the image
    buffer = io.BytesIO()
    code.write(buffer)
    buffer.seek(0)

    # Save the barcode image to a file
    barcode_image_file = f"{item_name}.png"
    with open(barcode_image_file, "wb") as f:
        f.write(buffer.getvalue())
    print(f"Barcode image saved to {barcode_image_file}")

    # Return the barcode image as a base64-encoded string
    barcode_image = buffer.getvalue()
    barcode_image_base64 = base64.b64encode(barcode_image).decode('utf-8')
    return jsonify({'barcode_image': barcode_image_base64})

if __name__ == '__main__':
    app.run(debug=True)