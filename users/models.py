from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.core.files import File
from PIL import Image


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
	prof_pic = models.ImageField(upload_to='prof_pics')
	image_url = models.URLField(null=True)
	bio = models.CharField(max_length=180,default='Welcome to SU-Learn')
	following = models.ManyToManyField(User,related_name="following")


	def get_remote_image(self):
		if self.image_url and not self.prof_pic:

			result = urllib.urlretrieve(self.image_url)
			self.prof_pic.save(
        		os.path.basename(self.image_url),
        		File(open(result[0]))
        		)
			self.save()\

	if prof_pic is not None:
		def save(self):
			super().save()
			img = Image.open(self.prof_pic.path)
			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(self.prof_pic.path)


	def get_absolute_url(self):
		return reverse('profile')



class CreatorProfile(models.Model):
	name = models.CharField(max_length=150)
	username = models.CharField(max_length=150,default='user1')
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	email = models.EmailField(null=True)
	dob = models.DateField(null=True)
	city = models.CharField(max_length=150)
	state = models.CharField(max_length=150)
	date_of_joining = models.DateTimeField(default=timezone.now)
	educational_qualifications = models.TextField()
	rating = models.FloatField(default=0)
	prof_pic = models.ImageField(upload_to='prof_pics')
	bio = models.CharField(max_length=180,default='Welcome to SU-Learn')
	followers = models.ManyToManyField(User,related_name="followers")


	def get_remote_image(self):
		if self.image_url and not self.prof_pic:

			result = urllib.urlretrieve(self.image_url)
			self.prof_pic.save(
        		os.path.basename(self.image_url),
        		File(open(result[0]))
        		)
			self.save()


	if prof_pic is not None:	
		def save(self):
			super().save()
			img = Image.open(self.prof_pic.path)

			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(self.prof_pic.path)





	def get_absolute_url(self):
		return reverse('profile')


