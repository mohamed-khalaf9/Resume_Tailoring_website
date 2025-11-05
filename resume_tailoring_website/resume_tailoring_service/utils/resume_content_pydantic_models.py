from pydantic import BaseModel, Field
from typing import Optional, List


class Account(BaseModel):
    platform: Optional[str] = Field(None)
    link: Optional[str] = Field(None)

class PersonalInfo(BaseModel):
    name: Optional[str] = Field(None)
    job_required_title: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    mobile_number: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    accounts: Optional[List[Account]] = Field(None)


class EducationItem(BaseModel):
    university_name: Optional[str] = Field(None)
    degree: Optional[str] = Field(None)
    specialization: Optional[str] = Field(None)
    faculty: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    start_date: Optional[str] = Field(None)
    end_date: Optional[str] = Field(None)
    related_coursework: Optional[Optional[List[str]]] = Field(None)
