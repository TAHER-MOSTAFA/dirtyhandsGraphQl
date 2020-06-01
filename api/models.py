from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class posts(models.Model):

    title = models.CharField(max_length=50)
    body = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)