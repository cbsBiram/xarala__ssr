from django.core.files.storage import FileSystemStorage
import base64

from django.core.files.base import ContentFile


def simple_upload(request, file):
    print(file, request.POST.get("file"), "oiijdik")
    if request.method == "POST" and request.FILES["files"]:
        files = request.FILES["files"]
        fs = FileSystemStorage()
        filename = fs.save(files.name, files)
        uploaded_file_url = fs.url(filename)
        print("up;load ", uploaded_file_url)
        return uploaded_file_url


def save_base_64(file):
    format, imgstr = file.split(";base64,")
    ext = format.split("/")[-1]
    data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
    return data
