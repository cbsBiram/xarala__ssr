from xarala.utils import SendSubscribeMail
from .models import Subscribe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "pages/index.html")


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email_id']
        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists():
            data = {"status": "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id=email)
            # Send the Mail, Class available in utils.py
            SendSubscribeMail(email)
    return HttpResponse("/")
