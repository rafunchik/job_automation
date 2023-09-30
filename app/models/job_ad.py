from pydantic import BaseModel
from typing import Annotated, Dict, List, Literal, Tuple


class JobAdInput(BaseModel):
    location: str
    keywords: str


class JobAdResponse(BaseModel):
    job_list: List[Dict[str, str]]
