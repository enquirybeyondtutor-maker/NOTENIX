from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    question_id: str
    answer: str


class TutorRequest(BaseModel):
    message: str


class ScheduleRequest(BaseModel):
    available_days: int = 7
