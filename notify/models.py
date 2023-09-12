from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """simple message model to send to another user"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    






