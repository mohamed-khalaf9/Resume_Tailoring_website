from pydantic import BaseModel, Field



class Account(BaseModel):
    platform: str = ""
    link: str =""

class PersonalInfo(BaseModel):
    name: str= ""
    job_required_title: str=""
    country: str=""
    city: str=""
    mobile_number: str=""
    email: str=""
    accounts: list[Account]=Field(default_factory=list)


class EducationItem(BaseModel):
    university_name: str=""
    degree: str=""
    specialization: str=""
    faculty: str=""
    country: str=""
    city: str=""
    start_date: str=""
    end_date: str=""
    related_coursework: list[str]=Field(default_factory=list)


class ExperienceItem(BaseModel):
    title: str=""
    company_name: str=""
    start_date: str=""
    end_date: str=""
    work_type: str=""
    location: str=""
    description: list[str]= Field(default_factory=list)


class ProjectLink(BaseModel):
    description: str=""
    link: str=""


class ProjectItem(BaseModel):
    name: str=""
    links: list[ProjectLink]= Field(default_factory=list)
    start_date: str=""
    end_date: str=""
    description: list[str]= Field(default_factory=list)


class SkillGroup(BaseModel):
    group_name: str=""
    skills: list[str]= Field(default_factory=list)


'''class AdditionalSectionItem(BaseModel):
    name: str=""
    start_date: str=""
    end_date: str=""
    link: str=""
    description: list[str]= Field(default_factory=list)


class AdditionalSection(BaseModel):
    section_title: str=""
    items: list[AdditionalSectionItem]= Field(default_factory=list)'''



class ResumeContent(BaseModel):
    personal_info: PersonalInfo=Field(default_factory=PersonalInfo)
    education: list[EducationItem]=Field(default_factory=list)
    experience: list[ExperienceItem]=Field(default_factory=list)
    projects: list[ProjectItem]=Field(default_factory=list)
    skills: list[SkillGroup]=Field(default_factory=list)





