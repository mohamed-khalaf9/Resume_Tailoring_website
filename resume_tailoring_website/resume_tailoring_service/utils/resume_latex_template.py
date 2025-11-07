from jinja2 import Template

from .resume_content_pydantic_models import *


def build_resume(resume: ResumeContent):

    resume_template = r"""
    
\begin{document}

%-----------PERSONAL INFORMATION-----------  

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

%-----------EDUCATION-----------


{% if education %}
\section{Education}
\resumeSubHeadingListStart
{% for education_item in education %}
    \resumeSubheading
      { {% if education_item.university_name %}
          {{ education_item.university_name }} University
        {% endif %} }
      
      { {%- if education_item.country and education_item.city -%}
          {{ education_item.country }}, {{ education_item.city }}
        {%- elif education_item.country -%}
          {{ education_item.country }}
        {%- elif education_item.city -%}
          {{ education_item.city }}
        {%- endif -%} 
      }
      
      {
        {%- if education_item.degree and education_item.faculty and education_item.specialization -%}
          {{ education_item.degree }} of {{ education_item.faculty }} in {{ education_item.specialization }}
        {%- elif education_item.degree and education_item.faculty and not education_item.specialization -%}
          {{ education_item.degree }} of {{ education_item.faculty }}
        {%- elif education_item.degree and education_item.specialization and not education_item.faculty -%}
          {{ education_item.degree }} in {{ education_item.specialization }}
        {%- elif education_item.faculty and education_item.specialization -%}
          {{ education_item.faculty }} in {{ education_item.specialization }}
        {%- elif education_item.degree -%}
          {{ education_item.degree }}
        {%- elif education_item.faculty -%}
          {{ education_item.faculty }}
        {%- elif education_item.specialization -%}
          {{ education_item.specialization }}
        {%- endif -%}
      }
      

      { {%- if education_item.start_date and education_item.end_date -%}
          {{ education_item.start_date }} -- {{ education_item.end_date }}
        {%- elif education_item.start_date -%}
          {{ education_item.start_date }}
        {%- else -%}
          {{ education_item.end_date }}
        {%- endif -%} 
      }

    {% if education_item.related_coursework %}
      \resumeItemListStart
        \resumeItem{\textbf{Related Coursework:} {{ education_item.related_coursework | join(", ") }} }
      \resumeItemListEnd
    {% endif %}

{% endfor %}
 \resumeSubHeadingListEnd
{% endif %}


    
    
    
    
    
    
    
    
    
    """

    template = Template(resume_template)
    resume_latex = template.render(resume.model_dump())
    print(resume_latex)