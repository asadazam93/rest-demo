"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest.messenger.views import MessageList, MessageDetail, RestaurantListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', MessageList.as_view()),
    path('messages/<pk>/', MessageDetail.as_view()),
    path("nearest_locations/<long>/<lat>/",
                      RestaurantListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
