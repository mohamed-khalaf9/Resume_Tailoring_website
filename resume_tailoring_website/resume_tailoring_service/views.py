from django.shortcuts import render

from .utils.LLM_integration import tailor_resume
from .utils.pdf_processing import extract_resume_content
from .utils.upload_form import UploadForm



def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            job_description = form.cleaned_data['job_description']
            resume_pdf_file = form.cleaned_data['resume_pdf_file']
            all_links_details,resume_content = extract_resume_content(resume_pdf_file.read())
            print("Resume Content########################################")
            print(resume_content)
            print("HyperLinkks############################################")
            print(all_links_details)
            tailored_resume_content = tailor_resume(resume_content,all_links_details,job_description)
            print("Tailored Resume Content############################################")
            print(tailored_resume_content)

        else:
            form = UploadForm()

    else:
        form = UploadForm()

    return render(request,'resume_tailoring/welcome.html',{'form':form})


