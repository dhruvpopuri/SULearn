from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import CourseCreateForm,ModuleCreateForm,VideoAddForm,CourseReviewForm
from django.template.defaultfilters import slugify
from .models import *
from users.models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import UpdateView,DeleteView
from taggit.models import Tag
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
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


def home(request):
	user = request.user
	if user.is_authenticated:
		return redirect(reverse('profile'))
	else:
		return render(request,'e_learning/index.html')



def creators(request):
	return render(request,'e_learning/Creator_home.html')

@user_passes_test(is_creator)
@login_required()
def CreateCourse(request):
	
	user = request.user



	if request.method == "POST" and CreatorProfile.objects.filter(user=user).count() != 0:
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
				email_ids.append(follower.learnerprofile.email)

			send_mail('Update!',f'A new course has just been uploaded by {creator}','learnerupdate16@gmail.com',

				email_ids)
			


			return redirect(reverse('course_details',kwargs={'slug':newcourse.slug}))


	else:
		form = CourseCreateForm()
	
	context = {
	'form':form
	}

	return render(request,'e_learning/create_course.html',context)

@login_required()
def mycourses(request):
	courses = Courses.objects.filter(created_by=request.user)
	context = {
	'courses':courses,
	}

	return render(request,'e_learning/mycourses.html',context)


@login_required()
def course_dets(request,slug):
	course = Courses.objects.get(slug=slug)
	slug = slug
	modules = course.modules.all()
	pk = course.pk
	creator = course.created_by
	#ENROLLMENT
	if f'enroll{pk}' in request.POST and LearnerProfile.objects.filter(user=request.user).count() != 0:
		user = request.user
		if user not in course.taken_by.all():
			course.taken_by.add(user)
			course.save()
		else:
			course.taken_by.remove(user)
			course.save()


	#Completion status of modules
	for module in modules:
		pk = module.pk
		user = request.user
		if f'{pk}' in request.POST and request.user in course.taken_by.all():
			if user in module.completed_by.all():
				module.completed_by.remove(user)
				module.save()
			else:
				module.completed_by.add(user)
				module.save()


	course_completion_statusq = []
	#Completion status of Courses
	for module in modules:
		if user in module.completed_by.all():
			course_completion_statusq.append('True')
		else:
			course_completion_statusq.append('False')


	if course_completion_statusq.count('False') == 0:
		user = request.user
		course.completed_by.add(user)
		course.save()

	else:
		user = request.user
		if user in course.completed_by.all():
			course.completed_by.remove(user)
			course.save()


				

	#To create module
	if request.method == "POST" and course.created_by == request.user :
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


	

	if module_completion_status_list.count('False') == 0 and LearnerProfile.objects.filter(user=request.user).count() != 0:
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

	if module_completion_status_list.count('False') == 0:
		test7 = True
	else:
		test7 = False

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
		iscreator = True
	else:
		iscreator = False

	for review in reviews:
		author = review.author
		author_list.append(author)
			 
	if request.user in author_list:
		reviewed = True
	else:
		reviewed = False


	#Allowing users to follow you
	if 'follow' in request.POST and LearnerProfile.objects.filter(user=user).count() != 0:
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

	#Follow button only for learners

	if LearnerProfile.objects.filter(user=user).count() != 0:
		test4 = True
	else:
		test4 = False


	#Frontend check for ability to complete a module
	if request.user in course.taken_by.all():
		enrolled = True
	else:
		enrolled = False

	if request.user in course.completed_by.all():
		completed = True
	else:
		completed = False

	print(course.completed_by.all())

	#To make it such that creator can't see enroll button for other courses
	if CreatorProfile.objects.filter(user=user).count() != 0:
		a_creator = True
	else:
		a_creator = False

 

	context = {
	'course':course,
	'form':form,
	'modules':modules,
	'slug':slug,
	'review_form':review_form,
	'reviews':reviews,
	#'test':test,
	'creator_followers':creator_followers,
	'test2':test2,
	'user':user,
	'test3':test3,
	'test4':test4,
	'enrolled':enrolled,
	'completed':completed,
	'iscreator':iscreator,
	'reviewed':reviewed,
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

def courses(request,page_num):
	courses = Courses.objects.all()
	user = request.user
	learnerprofiles = LearnerProfile.objects.all()
	creatorprofiles = CreatorProfile.objects.all()
	common_tags = Courses.tags.most_common()[:5]

	#Special provision for learners

	#if LearnerProfile.objects.filter(user=user).count() != 0:
		#learnerprofile = LearnerProfile.objects.get(user=user)
		#users_following = learnerprofile.following.all()
		#courses = Courses.objects.all()
		#courses_by_following = []
		#for creator in users_following:
			#course_of_creator = creator.created_by_set.all()
			#for course in course_of_creator:
				#courses_by_following.append(course)

		#Paginator for courses
		#paginator = Paginator(courses, 1)
		#page_objects = paginator.page(page_num)

		#Paginator for courses of followed creators
		#paginator_follow = Paginator(courses_by_following, 1)
		#page_following_objects = paginator.page
		
		#context={
		#'courses':courses,
		#'learnerprofile':learnerprofile,
		#'creatorprofiles':creatorprofiles,
		#'user':user,
		#'common_tags':common_tags,
		#'users_following':users_following,
		#'page_objects':page_objects,
		#'num_current':page_num,
		#'paginator':paginator,
		#}

		#return render(request,'e_learning/user_courses_view.html',context)


	#PAGINATION
	paginator = Paginator(courses, 1)

	page_objects = paginator.page(page_num)


	if request.method == "POST":
		page_objects = paginator.page(pk)	


		try:
			paginator.page(pk)
		except EmptyPage:
			paginator.page(1)



	if user in creatorprofiles:
		testx = True
	else:
		testx = False

	if LearnerProfile.objects.filter(user=user).count() != 0:
		learnere = True
	else:
		learnere = False	


	context={
	'courses':courses,
	'learnerprofile':learnerprofiles,
	'creatorprofiles':creatorprofiles,
	'user':user,
	'testx':testx,
	'common_tags':common_tags,
	'paginator':paginator,
	'page_objects':page_objects,
	'num_current':page_num,
	'learnere':learnere,


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
		post_names = Courses.objects.filter(name__contains=data)#Higher efficiency
		post_tags = Courses.objects.filter(tags__name__contains=data)
		sep_tags = post_names.union(post_tags)

		#for course in post_tags:
			#if course not in post_names:
				#sep_post_tags.append(course)


		#sep_tags = sep_post_tags


		
		user = request.user
		creatorprofiles = CreatorProfile.objects.all()


		context={
		'post_names':post_names,
		#'post_tags':post_tags,
		'user':user,
		'creatorprofiles':creatorprofiles,
		'sep_tags':sep_tags,
		}

		return render(request,'e_learning/search_results.html',context)

def tags(request,slug,page_num):	


	courses = Courses.objects.filter(tags__name__in=[slug])# *********


	paginator = Paginator(courses, 1)

	page_objects = paginator.page(page_num)


	if request.method == "POST":
		page_objects = paginator.page(pk)	


		try:
			paginator.page(pk)
		except EmptyPage:
			paginator.page(1)



	context = {
	'courses':courses,
	'slug':slug,
	'paginator':paginator,
	'page_objects':page_objects,
	'page_num':page_num,
	}
	return render(request,'e_learning/tag.html',context)


@login_required()
@user_passes_test(is_learner)
def courses_following(request,page_num):
		user = request.user

		learnerprofile = LearnerProfile.objects.get(user=user)
		users_following = learnerprofile.following.all()
		#courses = Courses.objects.all()
		courses_by_following = []
		for creator in users_following:
			course_of_creator = creator.created_by_set.all()
			for course in course_of_creator:
				if user not in course.taken_by.all():
					courses_by_following.append(course)


		#Paginator for courses
		paginator = Paginator(courses_by_following, 1)
		page_objects = paginator.page(page_num)

		#Check for you are already up to date
		#up_to_date = []
		#for course in courses_by_following:
			#if user in course.taken_by.all():
				#up_to_date.append(True)
			#else:
				#up_to_date.append(False)

		if courses_by_following == []:
			nocourses = True
		else:
			nocourses = False

		print(courses_by_following)
		print(page_objects)


		context={
		#'courses':courses,
		'learnerprofile':learnerprofile,
		#'creatorprofiles':creatorprofiles,
		'user':user,
		#'common_tags':common_tags,
		'users_following':users_following,
		'page_objects':page_objects,
		'num_current':page_num,
		'paginator':paginator,
		'nocourses':nocourses,
		}

		return render(request,'e_learning/user_courses_view.html',context)

	








