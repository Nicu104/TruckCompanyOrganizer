

from django.urls import re_path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path('^loginPage/$', views.log, name='loginpage'),
    
    re_path('^register/$', views.register, name='registerpage'),
    
    re_path('^registerForm$', views.registerForm, name='registerform'),
    
    re_path('^logIn/$', views.logIn, name='loginform'),

    re_path('^registernewuser$', views.newUser, name='registernewuser'),
    
    re_path('^tableLoads/$', views.loads, name='tableLoads'),
    
    re_path('^images/$', views.images, name='images'),
    
    # re_path('^about/$', views.about, name='about'),
    
    re_path('^logout/$', views.logout, name='logout'),
  
    re_path('^howitworks/$', views.howitworks, name='howitworks'),
    
    # re_path('^learnmore/$', views.learnmore, name='learnmore'),
    

    re_path('^adminpage/$', views.adminpage, name='adminpage'),
    
    re_path('^userpage/$', views.userpage, name='userPage'),
    
    re_path('^upload_pic', views.upload_pic, name='upload_pic'),
    
    re_path('^picturesLoad/(?P<id>\d+)/$', views.picturesLoad, name='picturesLoad'),
    
    re_path('', views.index, name='home'),

]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()