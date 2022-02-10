from django.http import HttpResponse
import os
from pathlib import Path

def my_image(request,image):
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    path2 = os.path.join(BASE_DIR, 'media','profile',image)
    image_data = open(path2, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")




