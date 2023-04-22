from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Obfuscate the image
def obfuscate_image(image):
    # Convert the image to a numpy array
    image_array = np.array(image)

    # Obfuscate the image by swapping the red and blue color channels
    image_array[:, :, [0, 2]] = image_array[:, :, [2, 0]]

    # Convert the numpy array back to an image
    obfuscated_image = Image.fromarray(image_array)

    return obfuscated_image

# Deobfuscate the image
def deobfuscate_image(image):
    # Convert the image to a numpy array
    image_array = np.array(image)

    # Deobfuscate the image by swapping the red and blue color channels back
    image_array[:, :, [0, 2]] = image_array[:, :, [2, 0]]

    # Convert the numpy array back to an image
    deobfuscated_image = Image.fromarray(image_array)

    return deobfuscated_image

# Render the upload page
@app.route('/')
def index():
    return render_template('index.html')

# Encrypt the image
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Get the image from the request
    image_file = request.files['image']
    image = Image.open(image_file)

    # Obfuscate the image
    obfuscated_image = obfuscate_image(image)

    # Convert the obfuscated image to base64
    buffered = io.BytesIO()
    obfuscated_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('ascii')

    # Return the obfuscated image as a JSON response
    return jsonify({'image': img_str})

# Decrypt the image
@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Get the obfuscated image from the request
    obfuscated_img_str = request.form['image']
    obfuscated_img_bytes = base64.b64decode(obfuscated_img_str)
    obfuscated_image = Image.open(io.BytesIO(obfuscated_img_bytes))

    # Deobfuscate the image
    deobfuscated_image = deobfuscate_image(obfuscated_image)

    # Convert the deobfuscated image to base64
    buffered = io.BytesIO()
    deobfuscated_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('ascii')

    # Return the deobfuscated image as a JSON response
    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)
