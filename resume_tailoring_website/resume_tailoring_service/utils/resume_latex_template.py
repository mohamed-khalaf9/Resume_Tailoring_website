from jinja2 import Template

from .resume_content_pydantic_models import *


def build_resume(resume: ResumeContent):

    resume_template = r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}  % New version (blue links)
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

{% if personal_info.name %}   
\begin{document}

%-----------PERSONAL INFORMATION-----------  


\begin{center}
   \textbf{\Huge \scshape {{ personal_info.name }} } \\ \vspace{1pt}


{% if personal_info.mobile_number %}
    \small {{ personal_info.mobile_number }} $|$ 
{% endif %}

{% if personal_info.country or personal_info.city %}
  {% if personal_info.country and personal_info.city %}
    {{ personal_info.country }}, {{ personal_info.city }}
  {% else %}
    {{ personal_info.country }}{{ personal_info.city }}
  {% endif %}
  $|$
{% endif %}

{% if personal_info.email %}
    \href{mailto:{{ personal_info.email }} }{\underline{ {{ personal_info.email }} } {% if personal_info.accounts %} $|$ {% endif %} 
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
{% if education_item.university_name %}
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
          {{ education_item.start_date }} -- Present
        {%- else -%}
          {{ education_item.end_date }}
        {%- endif -%} 
      }

    {% if education_item.related_coursework %}
      \resumeItemListStart
        \resumeItem{\textbf{Related Coursework:} {{ education_item.related_coursework | join(", ") }} }
      \resumeItemListEnd
    {% endif %}
{% endif %}
{% endfor %}

 \resumeSubHeadingListEnd
{% endif %}


{% if experience %}
%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart
  
{% for experience_item in experience %}

{%- if experience_item.title and experience_item.company_name -%}
    \resumeSubheading
         { {{ experience_item.title }} }
      { {%- if experience_item.start_date and experience_item.end_date -%}
          {{ experience_item.start_date }} -- {{ experience_item.end_date }}
        {%- elif experience_item.start_date -%}
          {{ experience_item.start_date }} -- Present
        {%- else -%}
          {{ experience_item.end_date }}
        {%- endif -%} 
      }
      { {%- if experience_item.company_name -%}
          {{ experience_item.company_name }}
        {%- endif -%} 
      }
      { {%- if experience_item.location -%}
          {{ experience_item.location }}
        {%- endif -%} 
      }
    {% if experience_item.description %}
      \resumeItemListStart
    {% for bullet in experience_item.description %}
        \resumeItem{ {{ bullet | safe }} }
    {% endfor %}
      \resumeItemListEnd
    {% endif %}
{% endif %}
{% endfor %}

  \resumeSubHeadingListEnd
{% endif %}


%-----------PROJECTS-----------
{% if projects %}
\section{Projects}
  \resumeSubHeadingListStart
  
{% for project in projects %}
  {% if project.name %} 

    \resumeProjectHeading
      {
        \textbf{ {{ project.name }} }
  
        {% if project.links %}
          $|$ 
          
          {% for link in project.links %}
            \href{ {{ link.link }} }{\underline{ {{ link.description }} }}
            {% if not loop.last %} $|$ {% endif %}
          {% endfor %}
        {% endif %}
      }
      
      {
        {%- if project.start_date and project.end_date -%}
          {{ project.start_date }} -- {{ project.end_date }}
        {%- elif project.start_date -%}
          {{ project.start_date }}
        {%- else -%}
          {{ project.end_date }}
        {%- endif -%}
      }
       
    {% if project.description %}   
      \resumeItemListStart
      {% for bullet in project.description %}
        \resumeItem{ {{ bullet | safe }} }
      {% endfor %}
      \resumeItemListEnd
    {% endif%}
      
  {% endif %}
{% endfor %}
  \resumeSubHeadingListEnd
{% endif %}

%-----------SKILLS-----------
{% if skills %}
\section{Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
 
    \small{
    \item{
{% for skill in skills %}
  {% if skill.group_name %}
     \textbf
     {
     {{ skill.group_name }}
     }
     {: 
     {{ skill.skills | join(", ") }}
     } 
     {% if not loop.last %} \\ {% endif %}
  {% endif %}
{% endfor %}
    }}  
    \noindent

 \end{itemize}
{% endif %}
    
%-----------ADDITIONAL SECTIONS-----------
{% if additional_sections %}
{% for additional_section in additional_sections %}
  {% if additional_section.section_title %}

    \section{ {{ additional_section.section_title | upper }} } 
      \resumeSubHeadingListStart
      
    {% for item in additional_section.items %}
      {% if item.name %} 
    
        \resumeProjectHeading
          {
            \textbf{ {{ item.name }} }
      
            {% if item.link %}
              $|$ 
              \href{ {{ item.link }} }{\underline{Link}} 
            {% endif %}
          }
          
          {
            {%- if item.start_date and item.end_date -%}
              {{ item.start_date }} -- {{ item.end_date }}
            {%- elif item.start_date -%}
              {{ item.start_date }} -- Present
            {%- else -%}
              {{ item.end_date }}
            {%- endif -%}
          }
           
        {% if item.description %}   
          \resumeItemListStart
          {% for bullet in item.description %}
            \resumeItem{ {{ bullet | safe }} }
          {% endfor %}
          \resumeItemListEnd
        {% endif%}
          
      {% endif %} 
    {% endfor %}
      \resumeSubHeadingListEnd
      
  {% endif %} 
{% endfor %} 
{% endif %} 

\end{document}
{% endif %}
    
    
    """

    template = Template(resume_template)
    resume_latex = template.render(resume.model_dump())
    print(resume_latex)