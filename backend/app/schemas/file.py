from pydantic import BaseModel
from datetime import datetime
class FileResponse(BaseModel):
    id: str
    openai_file_id: str
    filename: str
    purpose: str
    size_bytes: int | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}