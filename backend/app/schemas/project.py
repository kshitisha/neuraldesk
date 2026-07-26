from pydantic import BaseModel, Field
from datetime import datetime
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    system_prompt: str | None = None
    model: str = "gpt-4o"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    provider: str = "openai"
class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    system_prompt: str | None = None
    model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    provider: str | None = None
class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str | None
    system_prompt: str | None
    model: str
    temperature: float
    provider: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}