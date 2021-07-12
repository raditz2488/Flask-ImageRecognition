from flask import Flask, request, url_for, render_template
import os
from werkzeug import secure_filename
from tensorflow.keras.applications import MobileNet
from PIL import Image, ImageFile
from io import BytesIO
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions

# Declare a list of allowed file extensions
ALLOWED_EXTENSION = set(['txt', 'pdf', 'png','jpg','jpeg','gif'])

# Required image dimiensions
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3

# Function to check if extension of a file is allowed
def allowed_file(filename):
    # Split with '.' and maximum splits is 1
    return filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)