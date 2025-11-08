import io

from django.http import HttpResponse
from django.shortcuts import render, redirect


from .utils.LLM_integration import tailor_resume
from .utils.pdf_processing import extract_resume_content
from .utils.resume_content_pydantic_models import ResumeContent
from .utils.upload_form import UploadForm
from .utils.resume_latex_template import *
from django.core.cache import cache
from django.views.decorators.clickjacking import xframe_options_sameorigin




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
            resume: ResumeContent = tailor_resume(resume_content,all_links_details,job_description)
            print("Tailored Resume Content############################################")
            for item in resume:
                print("--------------------------------------------------------------------------------------")
                print(item)

            resume_latex = build_resume(resume)
            pdf_resume_bytes = compile_latex_to_pdf(resume_latex)

            if pdf_resume_bytes:
                cache_key = f'pdf_{request.session.session_key}'
                cache.set(cache_key,pdf_resume_bytes,timeout=6000)
                file_name_parts=[]
                if resume.personal_info.name:
                    name_part = "_".join(resume.personal_info.name.split())
                    file_name_parts.append(name_part)
                    if resume.personal_info.job_required_title:
                        title_part = "_".join(resume.personal_info.job_required_title.split())
                        file_name_parts.append(title_part)
                file_name = "_".join(file_name_parts)

                if not file_name:
                    file_name = "Tailored_Resume"

                return redirect("preview",file_name=file_name)
            else:
                form.add_error(None, "There was an error generating pdf")

    form = UploadForm()
    return render(request,'resume_tailoring/welcome.html',{'form':form})


def preview(request,file_name):
    return render(request,'resume_tailoring/preview.html',{'file_name':file_name})

@xframe_options_sameorigin
def pdf_preview(request):
    cache_key = f'pdf_{request.session.session_key}'
    resume_bytes = cache.get(cache_key)

    if resume_bytes:
        resume_pdf_file = io.BytesIO(resume_bytes)
        return HttpResponse(resume_pdf_file, content_type="application/pdf")
    else:
        return HttpResponse("There was an error generating pdf or session expired",status=404)


def pdf_download(request, file_name):
    cache_key = f'pdf_{request.session.session_key}'
    resume_bytes = cache.get(cache_key)

    if resume_bytes:
        resume_pdf_file = io.BytesIO(resume_bytes)
        response = HttpResponse(resume_pdf_file, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
        return response
    else:
        return HttpResponse("There was an error generating pdf or session expired")