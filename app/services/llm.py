from __future__ import annotations

import asyncio
from typing import List
from openai import OpenAI
from app.config import settings


def _age_bucket(age: int) -> str:
    if age <= 7:
        return "5-7"
    if age <= 11:
        return "8-11"
    if age <= 15:
        return "12-15"
    return "16-17"


def _build_system_prompt(age: int) -> str:
    bucket = _age_bucket(age)

    base = (
        "Ты — добрый и внимательный помощник для ребёнка {age} лет. "
        "Отвечай понятно и позитивно. Если встречается сложное слово — поясни его в скобках простыми словами. "
        "Опасные темы избегай и мягко перенаправляй на безопасные. "
    ).format(age=age)

    if bucket == "5-7":
        style = (
            "Стиль для 5–7 лет: используй 2–3 коротких предложения, простые слова, примеры из быта. "
            "Не более одного термина за ответ и сразу объясняй его в скобках."
        )
    elif bucket == "8-11":
        style = (
            "Стиль для 8–11 лет: 3–5 предложений, можно привести 1 факт или аналогию. "
            "Избегай длинных определений, делай вывод в конце одним предложением."
        )
    elif bucket == "12-15":
        style = (
            "Стиль для 12–15 лет: структурируй мысль в 2–3 пункта, давай простые определения, "
            "подталкивай к рассуждению («подумай, что будет если…»)."
        )
    else:  # "16-17"
        style = (
            "Стиль для 16–17 лет: короткая структура из пунктов — «что это», «почему так», «пример». "
            "Можно использовать термины с кратким определением. Без внешних ссылок."
        )

    return base + style


def _call_openai(messages: List[dict], model: str, temperature: float = 0.6) -> str:
    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()


async def generate_reply(age: int, question: str, context: list[str]) -> str:
    """
    Асинхронная обёртка над синхронным OpenAI-клиентом.
    Если ключ не задан или запрос упал — вернём безопасный фоллбек.
    """
    system = _build_system_prompt(age)
    messages = (
        [{"role": "system", "content": system}]
        + [{"role": "user", "content": c} for c in context[-6:]]
        + [{"role": "user", "content": question.strip()}]
    )

    if not settings.openai_api_key:
        return _fallback_answer(age, question)

    try:
        content = await asyncio.to_thread(
            _call_openai,
            messages=messages,
            model=settings.llm_model,
            temperature=0.6,
        )
        return content or _fallback_answer(age, question)
    except Exception:
        return _fallback_answer(age, question)


def _fallback_answer(age: int, question: str) -> str:
    tip = "Если хочешь, расскажу ещё простыми словами!" if age <= 7 else "Могу объяснить подробнее, скажи."
    head = "Интересный вопрос! " if question.strip().endswith("?") else ""
    return f"{head}Давай подумаем вместе: {question.strip()} {tip}"


