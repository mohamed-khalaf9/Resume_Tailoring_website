from django import forms




class UploadForm(forms.Form):
    job_description = forms.CharField(widget=forms.Textarea)
    resume_pdf_file = forms.FileField()