from django import forms




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