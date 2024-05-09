"""
URL configuration for Stock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.conf.urls import url
from stock_chat.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',login_page),
    path('login_page/',login_page,name='login_page'),
    path('login/',login,name='login'),
    path('register_page',register_page,name='register_page'),
    path('register/',register,name='register'),
    path('logout/',logout,name='logout'),
    path('home_page/',home_page,name='home_page'),
    path('analyze_page/',analyze_page,name='analyze_page'),
    path('chat_page/',chat_page,name='chat_page'),
    path('predict_analysis/',predict_analysis,name='predict_analysis'),
    path('process_message/',process_message,name='process_message'),
    path('my_view_page/',my_view_page,name='my_view_page'),

    # url(r'^admin/', admin.site.urls),
    # url(r'^$', login_page),
    # url(r'^login_page/', login_page, name='login_page'),
    # url(r'^login/', login, name='login'),
    # url(r'^register_page', register_page, name='register_page'),
    # url(r'^register/', register, name='register'),
    # url(r'^logout/', logout, name='logout'),
    # url(r'^home_page/', home_page, name='home_page'),
    # url(r'^analyze_page/', analyze_page, name='analyze_page'),
    # url(r'^chat_page/', chat_page, name='chat_page'),
    # url(r'^predict_analysis/', predict_analysis, name='predict_analysis'),
    # url(r'^process_message/', process_message, name='process_message'),
]
