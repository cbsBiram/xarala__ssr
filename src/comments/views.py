from django.http import HttpResponse


def all_comments(request):
    return HttpResponse("All comments")
