#Alle DTO / Schema Models werden hier definiert

from pydantic import BaseModel
from datetime import datetime

#class Post(BaseModel):
#    title: str
#    content: str
#    published: bool = True      #Feld mit Defaultwert

#class CreatePost(BaseModel):
#    title: str
#    content: str
#    published: bool = True

#class UpdatePost(BaseModel):
#    title: str
#    content: str
#    published: bool


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): # Nur Pass wird verwendet, wenn sonst keine neuen Felder zum PostBase hinzugefügt wird
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:           # Wird benötigt um ein ORM Model (SQLAlchemy Model) in ein pydantic Model umzuwandeln
        orm_mode = True

