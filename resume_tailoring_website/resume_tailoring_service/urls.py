from django.urls import path
from .views import *

urlpatterns = [
    path('tailor', upload, name='tailor'),
    path('preview', preview, name='preview'),

]