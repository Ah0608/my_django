from django.db import models


class User(models.Model):
    objects = models.Manager()

    gender = (
        ('male',"男"),
        ('female',"女"),
    )
    name = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True,max_length=50)
    sex = models.CharField(max_length=10,choices=gender,default='男')
    c_time = models.DateTimeField('创建日期',auto_now_add=True)


class EmailVerify(models.Model):
    objects = models.Manager()

    email_add = models.CharField(max_length=50)
    verify_code = models.CharField(max_length=10)
    expiration_time = models.IntegerField()
    is_used = models.BooleanField(default=False)