from pydantic import BaseModel


# Shared properties
# class Answer(BaseModel):
#     results : list  
class Answer(BaseModel):
    results : str  
    reference : list




