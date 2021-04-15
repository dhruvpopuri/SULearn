from django.urls import path
from . import views
from .views import CreatorUpdate

urlpatterns=[
	path('',views.profile,name='profile'),
	path('creator-update',views.CreatorUpdate,name="creator_update"),
	path('learner-update',views.LearnerUpdate,name="learner_update"),
	path('register/',views.register,name='register'),
	path('register/creator/',views.register_creator,name='register_creator'),
	path('register/learner/',views.register_learner,name='register_learner'),
	path('login/',views.login,name='login'),
	path('followers/',views.FollowersList,name='followers'),
	path('following/',views.FollowingList,name='following'),


] 