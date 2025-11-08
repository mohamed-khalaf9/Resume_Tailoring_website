from django.urls import path
from .views import *

urlpatterns = [
    path('tailor', upload, name='tailor'),
    path('preview', preview, name='preview'),
    path('preview/pdf', pdf_preview, name="serve_pdf_preview"),
    path('preview/pdf/download', pdf_download, name="serve_pdf_download"),

]