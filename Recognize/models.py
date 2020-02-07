from django.db import models
import os, io
from google.cloud import vision
from google.cloud.vision import types

# Create your models here.

def get_text(request, filename):

    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = "/home/adrian/Desktop/testUS/img/"
    IMAGE_FILE = filename
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as img_file:
        content = img_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    doc_text = response.full_text_annotation.text
