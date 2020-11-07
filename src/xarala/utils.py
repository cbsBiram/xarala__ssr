from django.conf import settings
from django.core.validators import EmailValidator
import mailchimp
import threading
import random
import os


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
