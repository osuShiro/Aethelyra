from django.db import models

# Create your models here.
class Chapter(models.Model):
    title=models.CharField(max_length=32)
    content=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title

class SessionLog(models.Model):
    rp_group=models.CharField(max_length=32)
    title=models.CharField(max_length=128)
    content=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.rp_group+': '+self.title