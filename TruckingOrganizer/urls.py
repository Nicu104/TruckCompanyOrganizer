
from django.urls import path, include

urlpatterns = [
    path('', include(('apps.main.urls', 'main'), namespace='main')),
]
