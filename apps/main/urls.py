

from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path('^loginPage/$', views.log, name='loginpage'),
    re_path('^register/$', views.register, name='registerpage'),
    re_path('^registerForm$', views.registerForm, name='registerform'),
    re_path('^logIn/$', views.logIn, name='loginform'),
    re_path('^about/$', views.about, name='about'),
    re_path('^howitworks/$', views.howitworks, name='howitworks'),
    re_path('^learnmore/$', views.learnmore, name='learnmore'),
    
    re_path('', views.index, name='home'),
    
]
