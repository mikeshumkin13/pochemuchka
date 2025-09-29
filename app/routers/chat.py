from fastapi import APIRouter
from app.schemas.chat import AskRequest, AskResponse
from app.services.moderation import is_safe
from app.services.llm import generate_reply
from app.services.limits import check_and_increment
from app.config import settings


router = APIRouter()

# простейший in-memory контекст (MVP)
_CONTEXT: dict[int, list[str]] = {}
_CHILD_AGE: dict[int, int] = {}

@router.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest) -> AskResponse:
    age = _CHILD_AGE.get(payload.child_id, 8)

    # NEW: дневной лимит
    allowed, used, limit = await check_and_increment(payload.child_id, settings.default_daily_limit)
    if not allowed:
        msg = (
            f"Лимит вопросов на сегодня исчерпан ({limit} в день). "
            "Спроси завтра — я буду ждать! 😊"
        )
        return AskResponse(reply=msg, dialog_id=payload.dialog_id or 0, blocked=True)

    if not is_safe(payload.message):
        return AskResponse(
            reply="Это тема для разговора со взрослыми. Давай обсудим что-то другое!",
            dialog_id=payload.dialog_id or 0,
            blocked=True,
        )

    history = _CONTEXT.setdefault(payload.child_id, [])
    reply = await generate_reply(age=age, question=payload.message, context=history)

    if not is_safe(reply):
        reply = "Поговорим о чём-то безопасном. Например, про космос или динозавров!"

    history.append(payload.message)
    history.append(reply)
    return AskResponse(reply=reply, dialog_id=payload.dialog_id or 0)


