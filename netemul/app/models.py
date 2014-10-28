from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
	tittle=models.CharField(max_length=100,unique=True)
	body=models.TextField()

	def __unicode__(self):
		return self.tittle
        
class User_login(models.Model):
	user_name = models.CharField(max_length=30)
	user_pass = models.CharField(max_length=30)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class PcDetails(models.Model):
	pc_name = models.CharField(max_length=30)
	pc_user = models.CharField(max_length=30)
	pc_ip = models.CharField(max_length=30)
	pc_password = models.CharField(max_length=30)
	pc_os = models.CharField(max_length=30)
	def __unicode__(self):
       		return self.pc_name
