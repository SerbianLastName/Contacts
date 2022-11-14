from pydantic import BaseModel
from typing import List, Optional

class ContactBase(BaseModel):    
    first_name: str
    last_name: Optional[str] = None
    cell_number: Optional[str] = None
    office_number: Optional[str] = None    
    home_number: Optional[str] = None
    email: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None    
    favorite: bool = False

# Extend ContactBase with id for db
# Not sure why tutorial does it this way
class ContactOnDB(ContactBase):    
    id_: str