from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Book(BaseModel):
    id: Optional[int] = None
    bookName: str
    rating: Optional[int] = None
    isPublished: bool = False
    publishedYear: Optional[int] = None
    created_at: Optional[datetime] = None

