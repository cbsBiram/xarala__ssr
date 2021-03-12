from django.core.files.storage import FileSystemStorage
import base64

from django.core.files.base import ContentFile


def simple_upload(request, file):
    if request.method == "POST" and request.FILES["files"]:
        files = request.FILES["files"]
        fs = FileSystemStorage()
        filename = fs.save(files.name, files)
        uploaded_file_url = fs.url(filename)
        return uploaded_file_url


def save_base_64(file):
    format, imgstr = file.split(";base64,")
    ext = format.split("/")[-1]
    data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
    return data
