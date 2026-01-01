from django.db import models

class register(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=120)
    password=models.CharField(max_length=120)




class Upload(models.Model):
    user_id=models.CharField(max_length=150)
    fileupload=models.CharField(max_length=150)
    result=models.CharField(max_length=120)
