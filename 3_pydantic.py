# Data validation
from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

# 1. Create Pydantic model
class Student(BaseModel):
    name : str = Field(max_length=20, description='Name of the student', default="N/A")
    age : int = Field(gt=0, lt=120, description='Age of the student')
    cgpa : float
    email: EmailStr
    hostel : bool
    interest : List[str]
    contact_detail : Optional[Dict[str, str]] = None # remove None or field ko khali chora to error ayi ga model_validation ki vja sa 


    # Custom Data Validation
    @field_validator('email')
    @classmethod
    def email_val(cls, value):
        if not str(value).endswith('.edu'):
            raise ValueError("Email must be .edu domain")
        return value

    @field_validator('name')
    @classmethod
    def name_val(cls, value):
        return value.upper()

    @field_validator('age')
    @classmethod
    def age_val(cls, value):
        if value > 100 or value < 0:
            raise ValueError("Age must be between 0 and 100")
        return value


    # Model Validator (field sa nikal kar model ki level pa validation)
    @model_validator(mode='after')
    # @classmethod
    def validdate_emergency_contact(model):
        if model.age > 20 and model.contact_detail:
            raise ValueError("Student must have a contact")
        else:
            return model
            
    
Student_info = {
    "name" : "abdullah",
    "age" : 100,
    'cgpa' : 3.9,
    'email': "xyz@uni.edu",
    'hostel' : False,
    'interest' : ["coding","gaming","music"],
    # 'contact_detail':{
    #     "phone": "1234567890",
    #     "email": "[EMAIL_ADDRESS]"
    # }
}
# 2.  Initialize pydantic object
std = Student(**Student_info)

def insert_student(student: Student):
    print(student)

# 3. Pass to function
insert_student(std)