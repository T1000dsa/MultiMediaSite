from pydantic import BaseModel, Field
from datetime import datetime


class SessionSchema(BaseModel):
    user_id: int
    expires_at: datetime