from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class MyUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True)
    def __str__(self):
        return str(self.username)
    
    # imageURL = models.URLField(blank=True, null=True)