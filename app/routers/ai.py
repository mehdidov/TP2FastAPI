from fastapi import APIRouter, Depends
from app.schemas.ai import AIRequest, AIResponse
from app.services.openrouter_client import chat_completion
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

# The authenticated user can communicate with the AI and receive a response.
@router.post("/chat", response_model=AIResponse)
async def chat_with_ai(
    data: AIRequest,
    current_user = Depends(get_current_user) 
):
    # Messages sent to the model
    messages = [
        {"role": "system", "content": "tu es un assistant"},
        {"role": "user", "content": data.prompt},
    ]

    response = await chat_completion(messages)

    return {"response": response}
