

from django.urls import path, include

urlpatterns = [
    path('', include('apps.main.urls')),
    # path('admin/', admin.site.urls),
]
