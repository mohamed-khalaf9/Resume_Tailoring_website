from jinja2 import Template

from .resume_content_pydantic_models import *


def build_resume(resume: ResumeContent):

    resume_template = r"""
    
    
    
    
    
    
    
    
    
    
    
    """

    template = Template(resume_template)
    resume_latex = template.render(resume.model_dump())
    print(resume_latex)