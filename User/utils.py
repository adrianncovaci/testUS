from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import os, io
from google.cloud import vision
from google.cloud.vision import types


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def read_text(filename):
    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = "/home/adrian/Desktop/testUS/"
    IMAGE_FILE = filename
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

    with io.open(FILE_PATH, 'rb') as img_file:
        content = img_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    doc_text = response.full_text_annotation.text
    return doc_text