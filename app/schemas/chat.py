from pydantic import BaseModel

class AskRequest(BaseModel):
    child_id: int
    message: str
    dialog_id: int | None = None

class AskResponse(BaseModel):
    reply: str
    dialog_id: int
    blocked: bool = False


