from django.db import models

# Create your models here.
class UserData(models.Model):

    username = models.CharField(max_length=100,null=False)

    email = models.EmailField(primary_key=True)
    password  =models.CharField(max_length =20,blank= False ,null= False)
    confirm_password = models.CharField(max_length= 20,blank= False,null = False)

    def __str__(self):
        return self.username

