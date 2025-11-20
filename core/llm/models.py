from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class LLMMessage(Base):
    __tablename__ = "llm_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # user input message
    prompt = Column(Text, nullable=False)

    # model output
    response = Column(Text, nullable=False)

    # timestamp automatically set
    created_at = Column(DateTime(timezone=True), server_default=func.now())