from pydantic import BaseModel, Field
from datetime import datetime
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=32000)
class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
    model_config = {"from_attributes": True}
class ConversationCreate(BaseModel):
    title: str | None = None
class ConversationResponse(BaseModel):
    id: str
    project_id: str
    title: str | None
    created_at: datetime
model_config = {"from_attributes": True}
class PromptCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
class PromptResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}