from pydantic import BaseModel


# Shared properties
class Quiz(BaseModel):
    results : dict


