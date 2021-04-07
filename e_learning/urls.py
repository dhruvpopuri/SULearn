from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
	path('',views.home,name='homepage'),
	path('courses',views.courses,name='courses'),
	path('creators/',views.creators,name="creator-home"),
	path('creators/create-course',views.CreateCourse,name='CreateCourse'),
	path('creators/mycourses',views.mycourses,name='mycourses'),
	path('courses/<slug:slug>',views.course_dets,name='course_details'),
	path('courses/<slug:slug>/<int:pk>/',views.module,name='module'),
	path('search/',views.search,name='search'),
	path('tags/<slug:slug>/',views.tags,name='tags')

]


urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
