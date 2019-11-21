from __future__ import unicode_literals
from django.db import models
import re


class photosManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not str(postData['img']).endswith('.jpg'):
            errors['img'] = "Images must be jpg"
        return errors

# Create your models here.
class photos(models.Model):
    img = models.ImageField(upload_to='media')
    objects = photosManager()

class imageDetect(models.Model):
    img = models.ImageField()