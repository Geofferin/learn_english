from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='home'),

    path('dictionary/', dictionary_view, name='dictionary'),
    path('learn_words/', learn_words, name='learn_words'),
]
