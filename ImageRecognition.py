from flask import Flask, request, url_for, render_template
import os
from werkzeug import secure_filename
from tensorflow.keras.applications import MobileNet
from PIL import Image, ImageFile
from io import BytesIO
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np

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
model = MobileNet(weights='imagenet', include_top=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('ImageML.html')

@app.route('/api/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return render_template('ImageML.html', prediction='No image posted. Should pass in attribute named image')

    file = request.files['image']

    if file.filename == '':
        return render_template('ImageML.html', prediction='You did not select an image')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        x = []
        ImageFile.LOAD_TRUNCATED_IMAGES = False

        # Load the image
        img = Image.open(BytesIO(file.read()))
        img.load()

        # Resize and preprocess the image data
        img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.ANTIALIAS)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Make the predictions
        pred = model.predict(x)

        # Decode the predictions for top 3 probabilities
        lst = decode_predictions(pred, top=3)

        # Prepare the response
        items = []
        for item in lst[0]:
            items.append({'name': item[1], 'prob': float(item[2])})

        response = {'pred': items}

        # Return the response in the template
        return render_template('ImageML.html', prediction=f'The image is most likely {response}')
    else:
        return render_template('ImageML.html', prediction='Invalid file extension')
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)