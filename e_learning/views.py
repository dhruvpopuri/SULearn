from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import CourseCreateForm,ModuleCreateForm,VideoAddForm,CourseReviewForm
from django.template.defaultfilters import slugify
from .models import *
from users.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView,DeleteView
from taggit.models import Tag
from django.core.mail import send_mail

# Create your views here.

def home(request):
	user = request.user
	if user.is_authenticated()== True:
		return render(reverse('profile'))
	else:
		return render(request,'e_learning/index.html')



def creators(request):
	return render(request,'e_learning/Creator_home.html')


@login_required
def CreateCourse(request):
	



	if request.method == "POST":
		form = CourseCreateForm(request.POST)

		if form.is_valid():
			form.instance.created_by = request.user 
			newcourse = form.save(commit=False)
			newcourse.slug = slugify(newcourse.name)
			newcourse.save()
			form.save_m2m()
			creator = newcourse.created_by
			followers = creator.creatorprofile.followers.all()
			email_ids = []
			for follower in followers:
				email_ids.append(follower.creatorprofile.email)

			send_mail('Update!',f'A new course has just been uploaded by {creator}','learnerupdate16@gmail.com',

				email_ids)
			


			return redirect(reverse('course_details',kwargs={'slug':newcourse.slug}))


	else:
		form = CourseCreateForm()
	
	context = {
	'form':form
	}

	return render(request,'e_learning/create_course.html',context)

@login_required
def mycourses(request):
	courses = Courses.objects.filter(created_by=request.user)
	context = {
	'courses':courses,
	}

	return render(request,'e_learning/mycourses.html',context)


@login_required
def course_dets(request,slug):
	course = Courses.objects.get(slug=slug)
	slug = slug
	modules = course.modules.all()
	pk = course.pk
	creator = course.created_by
	#ENROLLMENT
	if f'enroll{pk}' in request.POST:
		user = request.user
		if user not in course.taken_by.all():
			course.taken_by.add(user)
			course.save()
		else:
			course.taken_by.remove(user)
			course.save()


	#Completion status
	for module in modules:
		pk = module.pk
		user = request.user
		if f'{pk}' in request.POST:
			if user in module.completed_by.all():
				module.completed_by.remove(user)
				module.save()
			else:
				module.completed_by.add(user)
				module.save()


				

	#To create module
	if request.method == "POST":
		form = ModuleCreateForm(request.POST)
		if form.is_valid():
			form.instance.course = course
			module = form.save()

			pk = module.pk
			return redirect(reverse('module',kwargs={'slug':slug,'pk':pk}))

	else:
		form = ModuleCreateForm()

	#REVIEWS AND RATINGS


	module_completion_status_list = []
	for module in modules:
		user = request.user
		if user in module.completed_by.all():
			module_completion_status_list.append('True')
		elif user not in module.completed_by.all():
			module_completion_status_list.append('False')


	

	if module_completion_status_list.count('False') == 0:
		review_form = CourseReviewForm()

		if 'review' in request.POST:
			review_form = CourseReviewForm(request.POST)
			if review_form.is_valid():
				review_form.instance.review_course = course
				review_form.instance.author = request.user
				review_form.save()
				return redirect(reverse('course_details',kwargs={'slug':slug}))


	else:
		review_form = None



	#COURSE RATING
	reviews_list = course.reviews_set.all()
	ratings = []

	for review in reviews_list:
		ratings.append(review.review_rating)

	if len(ratings) == 0:
		rating = 0
	else:
		rating = sum(ratings)/len(ratings)
	
	course.rating = rating
	course.save()	

	



	#RESTRICTING CREATE MODULE TO THE CREATOR

	reviews = course.reviews_set.all()
	author_list = []  
	if request.user == course.created_by:
		test = True
	else:

		for review in reviews:
			author = review.author
			author_list.append(author)
			
		if request.user in author_list:
			test = True
		else:
			test = False


	#Allowing users to follow you
	if 'follow' in request.POST:
		creator = course.created_by
		user = request.user
		if user not in creator.creatorprofile.followers.all():
			creator.creatorprofile.followers.add(user)
			user.learnerprofile.following.add(creator)
		elif user in creator.creatorprofile.followers.all():
			creator.creatorprofile.followers.remove(user)
			user.learnerprofile.following.remove(creator)


	#Making it such that Creators dont see enroll button 
	if request.user == course.created_by:
		test2 = True
	else:
		test2 = False


	if request.user in CreatorProfile.objects.all():
		test3 = True
	else:
		test3 = False


	creator_followers = creator.creatorprofile.followers.all()
	user = request.user



 

	context = {
	'course':course,
	'form':form,
	'modules':modules,
	'slug':slug,
	'review_form':review_form,
	'reviews':reviews,
	'test':test,
	'creator_followers':creator_followers,
	'test2':test2,
	'user':user,
	'test3':test3,
	}

	return render(request,'e_learning/course_dets.html',context)


@login_required
def module(request,**kwargs): #This is the view for a single module.A detail page for a specific module you could say. #Better to use kwargs here since we have multiple slugs.Then while calling the kwarg we can specify the slug.
	module = Modules.objects.get(pk=kwargs['pk'])
	course = Courses.objects.get(slug=kwargs['slug'])
	videos = module.module_vids.all()
	slug = kwargs['slug']
	pk = kwargs['pk']
	name = course.name

	#Form to add name and video within the module
	if request.method == "POST":
		form = VideoAddForm(request.POST,request.FILES)
		if form.is_valid():
			form.instance.module = module
			form.save()
			
			return redirect(reverse('course_details',kwargs={'slug':slug}))


	else:
		form = VideoAddForm()

	if request.user == course.created_by:
		user_test = True
	else:
		user_test = False



	context={
	'module':module,
	'videos':videos,
	'form':form,
	'course':course,
	'user_test':user_test,
	'name':name,
	'slug':slug,


	}

	return render(request,'e_learning/module_dets.html',context)

def courses(request):
	courses = Courses.objects.all()
	user = request.user
	learnerprofile = LearnerProfile.objects.all()
	creatorprofiles = CreatorProfile.objects.all()
	common_tags = Courses.tags.most_common()[:5]

	if user in creatorprofiles:
		testx = True
	else:
		testx = False
	


	context={
	'courses':courses,
	'learnerprofile':learnerprofile,
	'creatorprofiles':creatorprofiles,
	'user':user,
	'testx':testx,
	'common_tags':common_tags,

	}

	return render(request,'e_learning/courses.html',context)


@login_required
def learners(request):
	courses = Courses.objects.all()
	context={
	'courses':courses,

	}

	return render(request,'e_learning/courses.html',context)

def search(request):
	if request.method == "POST":
		data = request.POST.get('search')
		post_names = Courses.objects.filter(name__contains=data)
		post_tags = Courses.objects.filter(tags__name__contains=data)
		sep_post_tags = []

		for course in post_tags:
			if course not in post_names:
				sep_post_tags.append(course)


		sep_tags = sep_post_tags


		user = request.user
		creatorprofiles = CreatorProfile.objects.all()


		context={
		'post_names':post_names,
		'post_tags':post_tags,
		'user':user,
		'creatorprofiles':creatorprofiles,
		'sep_tags':sep_tags
		}

		return render(request,'e_learning/search_results.html',context)

def tags(request,slug):	


	courses = Courses.objects.filter(tags__name__in=[slug])# *********

	context = {
	'courses':courses
	}
	return render(request,'e_learning/tag.html',context)







