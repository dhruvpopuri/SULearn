from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Courses(models.Model):
	name = models.CharField(max_length=180,null=True)
	overview = models.TextField(null=True)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='created_by_set')
	rating = models.FloatField(default=0)
	slug = models.SlugField(unique=True,max_length=100,null=True)
	tags = TaggableManager()
	taken_by = models.ManyToManyField(User)
	completed_by = models.ManyToManyField(User,related_name='completed_by')

	
	def get_absolute_url(self):
		return reverse('mycourses')

class Reviews(models.Model):
	review_course = models.ForeignKey(Courses,on_delete=models.CASCADE)
	review_text = models.TextField()
	review_rating = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(0)])
	author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Modules(models.Model):
	course = models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='modules')
	module_name = models.CharField(max_length=250)
	slug_mod = models.SlugField(unique=True,max_length=200,null=True)
	completed_by = models.ManyToManyField(User)


class Videos(models.Model):
	module = models.ForeignKey(Modules,on_delete=models.CASCADE,related_name='module_vids')
	name = models.CharField(max_length=200)
	videos = models.FileField(upload_to='videos/',null=True)
	completion_status = models.BooleanField(default=False)

	def __str__(self):
		return self.name



