from django.http import HttpResponse


def all_posts(request):
    return HttpResponse("All posts")
