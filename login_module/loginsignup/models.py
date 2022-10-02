from django.db import models

# Create your models here.


class users(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    email = models.EmailField( max_length = 254 )
    user_type_id = models.SmallIntegerField()
    userid = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.IntegerField()
    
    
class session(models.Model):
    session_id = models.CharField(max_length = 120)
    user_id = models.IntegerField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField()
    token = models.CharField(max_length=254)
    


