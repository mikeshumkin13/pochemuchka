from __future__ import annotations

import asyncio
from typing import List
from openai import OpenAI
from app.config import settings


def _build_system_prompt(age: int) -> str:
    base = (
        "Ты — добрый и внимательный помощник для ребёнка {age} лет. "
        "Отвечай коротко, понятно и позитивно. "
        "Если встречается сложное слово — поясни его в скобках простыми словами. "
        "Опасные темы избегай и мягко перенаправляй на безопасные."
    )
    return base.format(age=age)


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


