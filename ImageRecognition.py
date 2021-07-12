import flask import Flask, request, url_for, render_template
import os
from werkzeug import secure_filename
from tensorflow.keras.applications import MobileNet
from PIL import Image, ImageFile
from io import BytesIO
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions

