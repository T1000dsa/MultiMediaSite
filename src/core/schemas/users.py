from pydantic import BaseModel
from typing import Optional, Annotated

# For basic validation
class UserBase(BaseModel):
    login: str # Login for autorization
    username: Optional[str] # Username for public name. Can be none -> Anonymous 
    password: str
    mail: Optional[str]
    bio: Optional[str]

# For reading from database
class UserRead(UserBase):
    id:int