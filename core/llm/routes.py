from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import LLMMessage
from .schema import LLMRequest, LLMResponse, LLMRecord
from dependencies import get_db
from .service import llm_service

llm_router = APIRouter()


@llm_router.post('/', response_model=LLMRecord, status_code=201)
def llm_chat(message_data: LLMRequest, db: Session = Depends(get_db)) -> LLMRecord:
    """
    Endpoint to send a message to the LLM and save the conversation
    
    Args:
        message_data: The user's message (LLMRequest)
        db: Database session
        
    Returns:
        LLMRecord: The saved record with id, prompt and response
    """
    try:
        # Generate response using OpenAI service
        llm_response = llm_service.generate_response(message_data.prompt)
        
        # Create and save the message to the database
        message = LLMMessage(
            prompt=message_data.prompt,
            response=llm_response
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Return the record as LLMRecord
        return LLMRecord(
            id=str(message.id),
            prompt=message.prompt,
            response=message.response
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like OpenAI errors)
        raise
    except Exception as e:
        # Rollback on error
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )
