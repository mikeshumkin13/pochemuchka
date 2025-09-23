from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_children():
    # заглушка: вернём пустой список
    return []


