from django.db import models
from users.models import CustomUser

# Create your models here.


class UserLog(models.Model):
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=10)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_logs')

    def __str__(self):
        return f'{self.user.email}: {self.action}'