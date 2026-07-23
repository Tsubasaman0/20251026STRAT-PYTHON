from typing import Annotated

from pydantic import BaseModel, StringConstraints


QuestionText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=2000),
]


class QuestionRequest(BaseModel):
    question: QuestionText


class QuestionResponse(BaseModel):
    question: str
