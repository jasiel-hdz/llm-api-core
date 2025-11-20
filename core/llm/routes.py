from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import LLMMessage
from .schema import LLMRequest, LLMResponse, LLMRecord
from dependencies import get_db
# from .dependency import get_post_for_user
from openai import OpenAI

llm_router = APIRouter()

@llm_router.post('/')
def llm_chat(message_data: LLMRequest, db: Session = Depends(get_db)) -> LLMRecord:
    # message = LLMMessage(prompt=message_data,)
    # response = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": post_data.prompt}]
    # )

    # db.add(message)
    # db.commit()
    # return LLMRecord(
    #     id=message.id,
    #     prompt=message.prompt,
    #     response=message.response
    # )
    return LLMRecord(
        id=1,
        prompt="Hello, world!",
        response="Hello, world!"
    )
