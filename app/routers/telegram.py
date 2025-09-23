from fastapi import APIRouter

router = APIRouter()

@router.post("/update")
async def telegram_update():
    # заглушка под вебхук
    return {"ok": True}


