from django.urls import path
from .views import *

app_name='strona'

urlpatterns = [
    path('', index, name='index'),
    path('strona/nowy/', nowy, name='nowy'),
    path('strona/<int:pk>', wpis, name='wpis'),
    path('strona/<int:pk>/edit/', edycja, name='edycja'),
]
