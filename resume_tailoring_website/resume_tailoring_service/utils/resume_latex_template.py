from jinja2 import Template

from .resume_content_pydantic_models import *






test_resume = ResumeContent(
        personal_info=PersonalInfo(
            name="Mohamed Khalaf",
            country="Egypt",
            city="Cairo",
            mobile_number="+201094058512",
            email="mohamed.khalaf8340@gmail.com",
            accounts=[
                Account(platform="linkedin.com/in/mohamed-khalafcs111",
                        link="https://www.linkedin.com/in/mohamed-khalafcs111/"),
                Account(platform="github.com/mohamed-khalaf9", link="https://github.com/mohamed-khalaf9")
            ]
        ),
        education=[
            EducationItem(
                university_name="Minia",
                country="Egypt",
                city="Minya",
                degree="Bachelor",  # From "Bachelor of Science in Information Technology"
                faculty="Science",  # This is a guess, based on your model structure
                specialization="Information Technology",  # From "in Information Technology"
                start_date="Aug 2022",
                end_date="May 2026",
                related_coursework=[
                    "Data Structures", "Operating Systems", "Databases", "Networks", "Web Development",
                    "Object-Oriented Programming", "Cloud Computing"
                ]
            )
        ],
        experience=[
            ExperienceItem(
                title="Integration Engineer Intern",
                company_name="Cloudypedia",
                start_date="Jul 2025",
                end_date="Sep 2025",
                location="Remote",
                description=[
                    "Built expertise in API development and management with Apigee on Google Cloud",
                    "Built an API proxy securing backend endpoints for a major insurance firm and an identity-verification provider",
                    "Created a reusable shared flow for exchanging service-account data for access tokens, enabling external access without exposing credentials",
                    "Worked with fellow interns to debug and resolve critical Apigee policy issues, improving platform stability"
                ]
            ),
            ExperienceItem(
                title="LLMs Training Contributor",
                company_name="Outlier",
                start_date="Oct 2024",
                end_date="Feb 2025",
                location="Remote",
                description=[
                    "Created challenging AI prompts and assessed model responses, identifying weaknesses and providing structured feedback",
                    "Performed error analysis and wrote corrective responses to enhance model accuracy and reasoning",
                    r"Produced high-caliber prompts and responses using my experience in Java, OOP, SOLID principles, data structures"
                ]
            )
        ],
        projects=[
            ProjectItem(
                name="Multi-Threaded Http\_Server-From\_Scratch",
                links=[
                    ProjectLink(description="GitHub",
                                link="https://github.com/mohamed-khalaf9/Http_Server_From_Scratch"),
                    ProjectLink(description="Video Demo",
                                link="https://drive.google.com/file/d/10c0aOXKO-SD_Jd6fACGc4i4VbxbC-J_G/view?usp=sharing")
                ],
                start_date="Mar 2025",
                description=[
                    r"Built a multithreaded HTTP server in Java with efficient routing, file-serving endpoints, GZip compression, ETag caching, TCP keep-alive, and a security rate limiter for concurrent client requests.",
                    r"Integrated Log4j2 and Gson for logging and metrics, quantifying trade-offs and achieving $\approx$41\% bandwidth reduction with only $\approx$3\% latency overhead."
                ]
            ),
            ProjectItem(
                name="Shell-From-Scratch",
                links=[
                    ProjectLink(description="GitHub", link="https://github.com/mohamed-khalaf9/shell_from_scratch")
                ],
                start_date="Jan 2025",
                description=[
                    r"Developed a custom \textbf{Linux} shell in \textbf{C++} with core command execution (\texttt{ls}, \texttt{cd}, \texttt{pwd}) and raw input parsing",
                    r"Processed \textbf{full quoting support} (' ', '\" \"', \textbackslash\ escapes)",
                    r"Enabled basic \textbf{output redirection} (\texttt{>}, \texttt{>>}) via \texttt{cout} buffering control",
                    r"Designed \textbf{trie-based autocomplete} for fast command lookup from\textbf{ o(n) to o(k)} command lookup time complexity.",
                    r"\textbf{Debugged} parsing issues through manual testing"
                ]
            ),
            ProjectItem(
                name="E-Commerce Console Application",
                links=[
                    ProjectLink(description="GitHub", link="https://github.com/mohamed-khalaf9/E-Commerce-Console-App")
                ],
                start_date="Oct 2024",
                description=[
                    r"Constructed console-based e-commerce system in \textbf{Java} using \textbf{OOP principles} (encapsulation, inheritance)",
                    r"Customized \textbf{MVC architecture} for console applications, enabling isolated testing",
                    r"Implemented critical design patterns: \textbf{Singleton} for centralized inventory management and \textbf{Factory Method} for payment processor abstraction",
                    r"Enforced \textbf{SOLID principles} including \textbf{Dependency Inversion} for future-proof architecture",
                    r"\textbf{Collaborated} with a teammate via \textbf{Git Flow} (100+ commits), enforcing code review standards"
                ]
            )
        ],
        skills=[
            SkillGroup(group_name="Programming Languages", skills=["Java", "C++", "Python"]),
            SkillGroup(group_name="Frameworks", skills=["Spring Core", "Spring Boot"]),
            SkillGroup(group_name="Tools", skills=["Git/GitHub", "VS Code", "Linux"]),
            SkillGroup(group_name="Databases", skills=["SQL", "MySQL"]),
            SkillGroup(group_name="Languages", skills=["English (Advanced)", "Arabic (Native)"])
        ],
        additional_sections=[]  # Your .tex file did not contain any additional sections.
    )

def build_resume(resume: ResumeContent):
    resume_template = r"""
    {% raw %}
        \documentclass[letterpaper,11pt]{article}

    \usepackage{latexsym}
    \usepackage[empty]{fullpage}
    \usepackage{titlesec}
    \usepackage{marvosym}
    \usepackage[usenames,dvipsnames]{color}
    \usepackage{verbatim}
    \usepackage{enumitem}
    \usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}  
    \usepackage{fancyhdr}
    \usepackage[english]{babel}
    \usepackage{tabularx}
    % \input{glyphtounicode}
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
    \fancyhf{} 
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}


    \addtolength{\oddsidemargin}{-0.5in}
    \addtolength{\evensidemargin}{-0.5in}
    \addtolength{\textwidth}{1in}
    \addtolength{\topmargin}{-.5in}
    \addtolength{\textheight}{1.0in}

    \urlstyle{same}

    \raggedbottom
    \raggedright
    \setlength{\tabcolsep}{0in}


    \titleformat{\section}{
      \vspace{-4pt}\scshape\raggedright\large
    }{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]


    \pdfgentounicode=1



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
    {% endraw %}


    {% if personal_info.name %}   
    \begin{document}




    \begin{center}
       \textbf{\Huge \scshape {{ personal_info.name }} } \\ \vspace{1pt}{% if personal_info.mobile_number %}\small {{ personal_info.mobile_number }} $|$ {% endif %}{% if personal_info.country or personal_info.city %}{% if personal_info.country and personal_info.city %}{{ personal_info.country }}, {{ personal_info.city }}{% else %}{{ personal_info.country }}{{ personal_info.city }}{% endif %}$|${% endif %}{% if personal_info.email %}\href{mailto:{{ personal_info.email }} }{\underline{ {{ personal_info.email }} } } {%- if personal_info.accounts -%} $|$ {%- endif %}{%- endif -%}{%- if personal_info.accounts -%}{%- for account in personal_info.accounts -%}{%- if account.link and account.platform -%}\href{ {{ account.link }} }{\underline{ {{ account.platform }} }} {%- if not loop.last -%} $|$ {%- endif -%}{%- endif -%}{%- endfor -%}{%- endif %}\end{center}
    
{% if education %}
\section{Education}
\resumeSubHeadingListStart
  {% for education_item in education %}
    {% if education_item.university_name %}
      \resumeSubheading
        { {% if education_item.university_name %}{{ education_item.university_name }} University{% endif %} }{
        {%- if education_item.country and education_item.city -%}
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
        }{ 
        {%- if education_item.start_date and education_item.end_date -%}
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
\section{Experience}
  \resumeSubHeadingListStart
    {% for experience_item in experience %}
      {%- if experience_item.title and experience_item.company_name %}
    \resumeSubheading
      { {{ experience_item.title }} }{ {%- if experience_item.start_date and experience_item.end_date -%}
          {{ experience_item.start_date }} -- {{ experience_item.end_date }}
        {%- elif experience_item.start_date -%}
          {{ experience_item.start_date }} -- Present
        {%- else -%}
          {{ experience_item.end_date }}
        {%- endif -%} 
      }
      { {%- if experience_item.company_name -%}
          {{ experience_item.company_name }}
        {%- endif -%} }{ {%- if experience_item.location -%}
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
      {%- endif %}
    {% endfor %}
  \resumeSubHeadingListEnd
{% endif %}

{% if projects %}
\section{Projects}
  \resumeSubHeadingListStart
    {%- for project in projects -%}
      {%- if project.name -%} 
    \resumeProjectHeading
      { \textbf{ {{ project.name }} } {%- if project.links %} $|$ {%- for link in project.links -%} \href{ {{ link.link }} }{\underline{ {{ link.description }} }} {%- if not loop.last -%} $|$ {%- endif -%} {%- endfor -%} {%- endif -%} }{ {%- if project.start_date and project.end_date -%}{{ project.start_date }} -- {{ project.end_date }}{%- elif project.start_date -%}{{ project.start_date }}{%- else -%}{{ project.end_date }}{%- endif -%} }
        {%- if project.description -%}   
      \resumeItemListStart
          {% for bullet in project.description %}
        \resumeItem{ {{ bullet | safe }} }
          {% endfor %}
      \resumeItemListEnd
        {%- endif -%}
      {%- endif -%}
    {%- endfor -%}
  \resumeSubHeadingListEnd
{% endif %}

{%- if skills -%}
\section{Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \item \small
    {%- for skill in skills -%}
      {%- if skill.group_name -%}
         \textbf{ {{ skill.group_name }} }: {{ skill.skills | join(", ") }} {%- if not loop.last %} \\ {% endif -%}
      {%- endif -%}
    {%- endfor %}
 \end{itemize}
{%- endif -%}


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

                {%- if item.link -%}
                  $|$ 
                  \href{ {{ item.link }} }{\underline{Link}} 
                {%- endif -%}
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

    return resume_latex










if __name__ == "__main__":
    print("--- [TEST] Loading test_resume data... ---")
    # test_resume is imported from test_data.py
    print("--- [TEST] Data loaded. Calling build_resume()... ---")

    # Call the function with your test data
    final_latex_output = build_resume(test_resume)

    print("\n\n--- [SUCCESS] GENERATED LATEX OUTPUT: ---")
    print(final_latex_output)
    print("--- [END] END OF GENERATED LATEX ---")