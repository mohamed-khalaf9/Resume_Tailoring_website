from django.urls import path
from .views import *

urlpatterns = [
    path('', upload, name='tailor'),
    path('preview/<str:file_name>/', preview, name='preview'),
    path('preview/pdf', pdf_preview, name="serve_pdf_preview"),
    path('preview/pdf/download/<str:file_name>/', pdf_download, name="serve_pdf_download"),

]