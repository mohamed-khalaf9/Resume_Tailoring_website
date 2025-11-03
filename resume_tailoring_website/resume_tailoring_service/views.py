from django.shortcuts import render
from .utils.upload_form import UploadForm


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            job_description = form.cleaned_data['job_description']
            resume_pdf_file = form.cleaned_data['resume_pdf_file']
            print(type(resume_pdf_file))#debugging
            return
        else:
            form = UploadForm()

    else:
        form = UploadForm()

    return render(request,'resume_tailoring/welcome.html',{'form':form})


