from django.shortcuts import render
from django.http import HttpResponse


def all_courses(request):
    return HttpResponse("All courses")
