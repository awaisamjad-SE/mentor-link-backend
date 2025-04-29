
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('contactapp.urls')),
    path('api/courses/', include('courses.urls')), 
    path('api/chat/', include('chat.urls')),
]
