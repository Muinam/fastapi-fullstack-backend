from typing import Literal
from pydantic import BaseModel


class Address(BaseModel):
    city : str
    pin_code : int

class Student(BaseModel):
    name : str
    gender : Literal["male","female"] # Literal ka use tab hota hai jab tum chahte ho ke kisi field mein sirf specific, predefined values hi allowed hon.
    address : Address


student_data = {
    "name": "Abdullah",
    "gender": "male",
    "address": {
        "city": "Karachi",
        "pin_code": 123456
    }
}

student = Student(**student_data)

# Pydantic form
# print(student.name)
# print(student.gender)
# print(student.address)

# Dict form
temp = student.model_dump()
print(temp)
print(type(temp))


# JSON form
json_data = student.model_dump_json() # include or exclude use for data ko remove 
print(json_data)
print(type(json_data))