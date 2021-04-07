from django import forms
from django.contrib.auth.models import User
from .models import Courses,Modules,Videos,Reviews

class CourseCreateForm(forms.ModelForm):

	class Meta:
		model = Courses
		fields = ['name','overview','tags']

class ModuleCreateForm(forms.ModelForm):

	class Meta:
		model = Modules
		fields = ['module_name']


class VideoAddForm(forms.ModelForm):


	class Meta:
		model = Videos
		fields = ['name','videos']

class CourseReviewForm(forms.ModelForm):

	class Meta:
		model = Reviews
		fields = ['review_text','review_rating']