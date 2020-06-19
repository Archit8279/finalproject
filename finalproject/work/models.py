from django.db import models

# Create your models here.
class users(models.Model):
    uid = models.IntegerField(primary_key = True)
    uname = models.CharField(max_length = 20)
    pwd = models.CharField(max_length = 20)
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)
    mob = models.CharField(max_length = 10)
    email = models.CharField(max_length = 100,unique = True)
    dob = models.DateField()
    age = models.IntegerField()
    otp = models.IntegerField()
    romantic = models.CharField(max_length = 20)
    action = models.CharField(max_length = 20)
    comedy = models.CharField(max_length = 20)
    animation = models.CharField(max_length = 20)
    horror = models.CharField(max_length = 20)

