from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .validations import clean_text


class UploadForm(forms.Form):
    job_description = forms.CharField(
        widget=forms.Textarea,max_length = 6000,
        min_length= 1000,strip =True,label='The Job Description',
        required=True,
        help_text='Enter your job details here...', )

    resume_pdf_file = forms.FileField(
        label='The Resume File(PDF)',required=True,
        help_text='Please upload a PDF file under 5MB.',
        max_length=100,
        validators=[FileExtensionValidator(['pdf'])]

    )


    def clean_job_description(self):
        job_description = self.cleaned_data['job_description']
        job_description = clean_text(job_description)
        return job_description

# check difference between .get and square bracket in dictionary to access value
    def clean_resume_pdf_file(self):
        resume_pdf_file = self.cleaned_data['resume_pdf_file']
        MAX_SIZE_MB = 6
        if resume_pdf_file.size > MAX_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Resume file must not exceed {MAX_SIZE_MB} MB")

        return resume_pdf_file



