from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FeedbackModel(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='', default='write your feedback here...')

    def snippet(self):
        return self.body[:30] + '...'

    def __str__(self):
        return self.snippet()
