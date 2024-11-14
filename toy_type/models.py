from django.db import models

class Toy_type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
#获取实例
    def __str__(self):
        return self.name