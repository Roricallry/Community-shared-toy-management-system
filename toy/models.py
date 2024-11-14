from django.db import models

# Create your models here.

class Toy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=1)
    toy_donor = models.CharField(max_length=10)
    applicable_age = models.IntegerField(10)
    image_path = models.CharField(max_length=100, default='default_image.jpg')

