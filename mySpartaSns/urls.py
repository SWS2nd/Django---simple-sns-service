"""mySpartaSns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from . import views # 지금 내가 있는 폴더에서 views라는 파이썬 파일을 가져올 거야. 라는 것.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.base_response, name='first_test'),
    path('first/', views.first_view, name='first_view'),
    path('', include('user.urls')),
    path('', include('tweet.urls')),
]
