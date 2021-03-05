import os
import base64
import random
import string
import threading

import mailchimp
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import EmailValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9347326742427)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


class SendSubscribeMail(object):
    def __init__(self, email):
        self.email = email
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        API_KEY = settings.MAILCHIMP_API_KEY
        LIST_ID = settings.MAILCHIMP_SUBSCRIBE_LIST_ID
        api = mailchimp.Mailchimp(API_KEY)
        try:
            api.lists.subscribe(LIST_ID, {"email": self.email})
        except Exception:
            return False


def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value


def generate_key():
    key = "".join(random.choices(string.digits, k=4))
    return key


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def save_base_64(file):
    format, imgstr = file.split(";base64,")
    ext = format.split("/")[-1]
    data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
    return data


def format_date(date_object):
    day = date_object.strftime("%a")
    day_of_month = date_object.strftime("%d")
    month = date_object.strftime("%b")
    year = date_object.strftime("%Y")
    return "{} {} {} {}".format(day, day_of_month, month, year)
