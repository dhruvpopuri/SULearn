from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from .forms import (CreatorCreateForm,
	LearnerCreateForm,
	CreatorUserUpdateForm,
	CreatorProfileUpdateForm,
	LearnerUserUpdateForm,
	LearnerProfileUpdateForm)
from django.views.generic import CreateView
from allauth.socialaccount.models import SocialAccount
from e_learning.models import Courses
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from e_learning.models import Modules
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def is_learner(user):
	if LearnerProfile.objects.filter(user=user).count() != 0:
		return True
	else:
		return False

def is_creator(user):
	if CreatorProfile.objects.filter(user=user).count() != 0:
		return True
	else:	
		return False


@login_required
def profile(request):
	user = request.user
	learner_profile = LearnerProfile.objects.filter(user=user)
	creator_profile = CreatorProfile.objects.filter(user=user)


	if learner_profile.count() == 0 and creator_profile.count() == 0 :

		return redirect('register')


	if learner_profile.count() != 0 and creator_profile.count() == 0 :
		profile = LearnerProfile.objects.get(user=user)
		name = profile.name
		DOB = profile.dob
		dob = DOB.date()
		dob2 = dob.strftime('%d/%m/%Y')
		city = profile.city 
		state = profile.state
		date_of_joining = profile.date_of_joining
		prof_pic = profile.prof_pic
		bio = profile.bio
		#To get default picture
		social_account = SocialAccount.objects.get(user=user)
		#img_url = social_account.extra_data['picture'] 
		email = social_account.extra_data['email']
		profile.email = email
		profile.save()

		#Courses taken

		courses_taken = user.courses_set.all()
		#for course in courses_taken:			
			#modules = course.modules.all()
			#course_completion_status = []
			#for module in modules:
				#if user in module.completed_by.all():
					#course_completion_status.append('True')
				#else:
					#course_completion_status.append('False')


			#if course_completion_status.count('False') == 0:
				#course.completed_by.add(user)
				#course.save()

			#else:
				#if user in course.completed_by.all():
					#course.completed_by.remove(user)
					#course.save()

		#Following
		following_count = user.learnerprofile.following.count()

		email = profile.email
		

		context = {
		'profile':profile,
		#'name':name,
		'DOB':dob2,
		#'city':city,
		#'state':state,
		#'date_of_joining':date_of_joining,
		#'email':email,
		#'img_url':img_url,
		'prof_pic':prof_pic,
		'bio':bio,
		'courses':courses_taken,
		'following_count':following_count,
		'user':user



		}
		

		return render(request,'users/Learner_Profile.html',context)

	if learner_profile.count() == 0 and creator_profile.count() != 0 :
		profile = CreatorProfile.objects.get(user=user)
		name = profile.name
		DOB = profile.dob
		dob = DOB.date()
		dob2 = dob.strftime('%d/%m/%Y')
		city = profile.city
		state = profile.state
		date_of_joining = profile.date_of_joining
		educational_qualifications = profile.educational_qualifications
		profile.email = user.email
		profile.save()
		email = profile.email
		prof_pic = profile.prof_pic
		bio = profile.bio
		#To get default profile pic

		social_account = SocialAccount.objects.get(user=user)
		img_url = social_account.extra_data['picture']
		#Courses created by this creator
		courses = user.created_by_set.all()
		#Creator Rating
		ratings = []
		for course in courses:
			rating = course.rating
			ratings.append(rating)

		if len(ratings) == 0:
			user_rating=0
		else:
			user_rating = sum(ratings)/len(ratings)
		#Followers Count
		follower_count = user.creatorprofile.followers.count()


		context = {
		'profile':profile,
		#'name':name,
		'DOB':dob2,
		#'city':city,
		#'state':state,
		#'date_of_joining':date_of_joining,
		#'educational_qualifications':educational_qualifications,
		#'email':email,
		'img_url':img_url,
		'prof_pic':prof_pic,
		'bio':bio,
		'courses':courses,
		'user_rating':user_rating,
		'follower_count':follower_count,



		}

		return render(request,'users/Creator_Profile.html',context)



def login(request):
	return render(request,'users/login.html')




def register(request):
	return render(request,'users/register.html')


def register_creator(request,**kwargs):
	if request.method == "POST":
		form = CreatorCreateForm(request.POST)
		if form.is_valid():
			form.instance.user = request.user

			form.save()
			return redirect('profile')

	else:
		form = CreatorCreateForm()


	context = { 
		'form':form
		}


	return render(request,'users/registration_page.html',context)


def register_learner(request,**kwargs):
	if request.method == 'POST':
		form = LearnerCreateForm(request.POST)

		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('profile')


	else:
		form = LearnerCreateForm()

	context = {
		'form':form
		}
	return render(request,'users/registration_page.html',context)


@user_passes_test(is_creator)
@login_required()
def CreatorUpdate(request):
	user = request.user
	creatorprofiles = CreatorProfile.objects.all()
	profile = CreatorProfile.objects.get(user=user)
	u_form = CreatorUserUpdateForm(instance=user)
	p_form = CreatorProfileUpdateForm(instance=profile)

	if request.method == "POST":
		u_form = CreatorUserUpdateForm(request.POST,instance=user,)
		p_form = CreatorProfileUpdateForm(request.POST,request.FILES,instance=profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('profile')


 
	context={
	'user':user,
	'u_form':u_form,
	'p_form':p_form,
	'creatorprofiles':creatorprofiles
	}

	return render(request,'users/creator_update.html',context)

@user_passes_test(is_learner)
@login_required()
def LearnerUpdate(request):
	user = request.user
	creatorprofiles = CreatorProfile.objects.all()
	profile = LearnerProfile.objects.get(user=user)
	u_form = LearnerUserUpdateForm(instance=user)
	p_form = LearnerProfileUpdateForm(instance=profile)

	if request.method == "POST":
		u_form = LearnerUserUpdateForm(request.POST,instance=user,)
		p_form = LearnerProfileUpdateForm(request.POST,request.FILES,instance=profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('profile')



	context={
	'user':user,
	'u_form':u_form,
	'p_form':p_form,
	'creatorprofiles':creatorprofiles
	}

	return render(request,'users/creator_update.html',context)


@user_passes_test(is_creator)
@login_required()
def FollowersList(request):
	user = request.user
	creatorprofile = CreatorProfile.objects.get(user=user)
	followers = creatorprofile.followers.all()

	context={
	'followers':followers,

	}

	return render(request,'users/followers.html',context)




@user_passes_test(is_learner)
@login_required()
def FollowingList(request):
	user = request.user
	learnerprofile = LearnerProfile.objects.get(user=user)
	following = learnerprofile.following.all()

	context={
	'following':following,

	}

	return render(request,'users/following.html',context)