"""WebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Student import views
from django.urls import path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
def lessons_view(request):
    return render(request, 'lessons.html')
def test_view(request):
    return render(request, 'test.html')

def city_view(request):
    return render(request, 'city.html')

urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('admin/', admin.site.urls),
    path("", views.index, name='home'),
    path('lessons/', views.index, name='lessons'),
    path('lesson/', views.lesson, name='lesson'),
    path('test/', test_view, name='test'),
    path('city/', city_view, name='city'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

