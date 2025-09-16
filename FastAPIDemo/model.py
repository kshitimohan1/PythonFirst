from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: Optional[int] = None
    bookName : str
    rating : int
    published: bool = True
    year: Optional[int] = None