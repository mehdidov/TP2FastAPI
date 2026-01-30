from pydantic import BaseModel

# Schema of the request sent to AI 
class AIRequest(BaseModel):
    prompt: str

# Schema of the response returned by AI
class AIResponse(BaseModel):
    response: str
