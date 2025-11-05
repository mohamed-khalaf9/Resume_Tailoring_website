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


