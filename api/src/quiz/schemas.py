from pydantic import BaseModel


# Shared properties
class Quiz(BaseModel):
    results : list  #[quiz,answer]

class Translate_Quiz(BaseModel):
    results : str


