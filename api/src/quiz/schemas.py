from pydantic import BaseModel


# Shared properties
class Quiz(BaseModel):
    results : str  
    answer : list   #[quiz1, quiz2, ...]

class Translate_Quiz(BaseModel):
    results : str
