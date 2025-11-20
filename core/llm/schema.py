from pydantic import BaseModel

class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    response: str
    
class LLMRecord(BaseModel):
    id: str
    prompt: str
    response: str

    class Config:
        from_attributes = True