
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def get_temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())