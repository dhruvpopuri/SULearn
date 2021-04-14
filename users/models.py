from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
import os
from django.core.files import File
from PIL import Image
from allauth.socialaccount.models import SocialAccount
import os.path
from SU_Learn.settings import MEDIA_ROOT



# Create your models here.

class LearnerProfile(models.Model):
	name = models.CharField(max_length=150)
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	username = models.CharField(max_length=150,default='user1')
	email = models.EmailField(null=True)
	dob = models.DateTimeField()
	city = models.CharField(max_length=150)
	state = models.CharField(max_length=150)
	date_of_joining = models.DateTimeField(default=timezone.now)
	prof_pic = models.ImageField(upload_to='prof_pics',null=True,blank=True)
	#image_url = models.URLField(null=True)
	bio = models.CharField(max_length=180,default='Welcome to SU-Learn')
	following = models.ManyToManyField(User,related_name="following")


	def get_image_url(self):
		if self.prof_pic:
			return self.prof_pic.url


		social_account = SocialAccount.objects.get(user=self.user)

		return social_account.extra_data['picture']






	def save(self,*args,**kwargs):
				
		if self.prof_pic:
			path = self.prof_pic.path
			path_list = path.split('/')
			pathq = path_list[2:]
			true_path = '/SU_Learn/' + ('/'.join(pathq))
			img = Image.open(true_path)
			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(true_path)			
		super().save(*args,**kwargs)


	def get_absolute_url(self):
		return reverse('profile')



class CreatorProfile(models.Model):
	name = models.CharField(max_length=150)
	username = models.CharField(max_length=150,default='user1')
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	email = models.EmailField(null=True)
	dob = models.DateTimeField(null=True)
	city = models.CharField(max_length=150)
	state = models.CharField(max_length=150)
	date_of_joining = models.DateTimeField(default=timezone.now)
	educational_qualifications = models.TextField()
	rating = models.FloatField(default=0)
	prof_pic = models.ImageField(upload_to='prof_pics',null=True,blank=True)
	bio = models.CharField(max_length=180,default='Welcome to SU-Learn')
	followers = models.ManyToManyField(User,related_name="followers")


	def get_image_url(self):
		if self.prof_pic:
			return self.prof_pic.url


		social_account = SocialAccount.objects.get(user=self.user)

		return social_account.extra_data['picture']






	def save(self,*args,**kwargs):
		print(self.prof_pic)
		if self.prof_pic:
			img = Image.open(MEDIA_ROOT + self.prof_pic.path)
			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(MEDIA_ROOT + self.prof_pic.path)
		super().save(*args,**kwargs)



	def get_absolute_url(self):
		return reverse('profile')


