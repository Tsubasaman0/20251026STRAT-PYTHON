from fastapi import APIRouter

from app.models.question import QuestionRequest, QuestionResponse


router = APIRouter(prefix="/api", tags=["questions"])


@router.post("/questions", response_model=QuestionResponse)
async def echo_question(payload: QuestionRequest) -> QuestionResponse:
    """Return the submitted question until AI integrations are added."""
    return QuestionResponse(question=payload.question)
