from jinja2 import Template

from .resume_content_pydantic_models import *


def build_resume(resume: ResumeContent):

    resume_template = r"""
    
\begin{document}
    
\begin{center}

{% if personal_info.name %}
    \textbf{\Huge \scshape {{ personal_info.name }} } \\ \vspace{1pt}
{% endif%}

{% if personal_info.mobile_number %}
    \small {{ personal_info.mobile_number }} $|$ 
{% endif %}

{% if personal_info.country %}
{{ personal_info.country }},
{% endif %}

{% if personal_info.city %}
{{ personal_info.city }} $|$  
{% endif %}

{% if personal_info.email %}
    \href{mailto:{{ personal_info.email }} }{\underline{ {{ personal_info.email }} } $|$ 
{% endif %}
    
{% if personal_info.accounts %}
{% for account in personal_info.accounts %}
{% if account.link and account.platform %}
    \href{ {{ account.link }} }{\underline{ {{ account.platform }} }}
    {% if not loop.last %} $|$ {% endif %}
{% endif %}
{% endfor %}
{% endif %}
\end{center}


    
    
    
    
    
    
    
    
    
    """

    template = Template(resume_template)
    resume_latex = template.render(resume.model_dump())
    print(resume_latex)