from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

class CreatorCreateForm(forms.ModelForm):

	class Meta:
		model = CreatorProfile
		fields = ['name','dob','city','state','educational_qualifications'] #Better to use forms.ModelForm than UserCreationForm as UserCreationForm has mandatory fields.
																			#forms.ModelForm is more customisable

class LearnerCreateForm(forms.ModelForm):

	class Meta:
		model = LearnerProfile
		fields = ['name','dob','city','state']


class CreatorUserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username','email']

class CreatorProfileUpdateForm(forms.ModelForm):


	class Meta:
		model = CreatorProfile
		fields = ['bio','city','state','educational_qualifications','prof_pic']


class LearnerUserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username','email']

class LearnerProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = CreatorProfile
		fields = ['bio','city','state','prof_pic']





