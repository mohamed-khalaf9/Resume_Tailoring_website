from django import forms

from resume_tailoring_website.resume_tailoring_service.utils.validations import clean_text


class UploadForm(forms.Form):
    job_description = forms.CharField(
        widget=forms.Textarea,max_length = 6000,
        min_length= 1000,strip =True,label='The Job Description',
        required=True,
        help_text='Enter your job details here...', )

    resume_pdf_file = forms.FileField(
        label='The Resume File(PDF)',required=True,
        help_text='Please upload a PDF file under 5MB.',
        max_length=100, )


    def clean_job_description(self):
        job_description = self.cleaned_data['job_description']
        job_description = clean_text(job_description)
        return job_description


