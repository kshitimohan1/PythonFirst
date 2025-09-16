from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Book(BaseModel):
    id: Optional[int] = None
    bookName: str
    rating: Optional[float] = None
    isPublished: Optional[bool] = False
    publishedYear: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }