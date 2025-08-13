import datetime
import re
from pydantic import BaseModel, Field, EmailStr


class UserDetails(BaseModel):
    name: str = Field(default=None, description="Name of the candidate")
    email: EmailStr = Field(default=None, description="Email address of the candidate")
    phone: str = Field(default=None, description="Valid contact number of the candidate with country code if avilable")
    skills: str = Field(default=None, description="Skills/technologies from the resume")
    work_related_skills: str = Field(default=None, description="Skills/technologies mentioned in work experience and project section, dont include sills from skill section of resume")
    current_company: str = Field(default=None, description="Extract recent company candidate worked or working from experience section")
    current_location: str = Field(default=None, description="Extract recent work location of candidate worked or working from experience section")
    total_work_experience: int = Field(default=None, description=f"Calculate candidate's total years of working experience from start date of career date till today's date {datetime.date.today().strftime('%m/%d/%Y')}. \
                                                                             if candidate in not working in any company then calculate from start date of career to last date he had worked. If there are career gpas then do not consider that period" )
    education: str = Field(default=None, description="Heighest education of the candidate, if there are multiple degrees then extract the highest degree")
