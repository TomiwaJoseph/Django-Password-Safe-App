from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class SavedPassword(models.Model):
    website = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    saver = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.saver)+' - '+str(self.website)