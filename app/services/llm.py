async def generate_reply(age: int, question: str, context: list[str]) -> str:
    # MVP-заглушка: короткий «умный» ответ без LLM
    if question.strip().endswith("?"):
        base = "Интересный вопрос! "
    else:
        base = ""

    tip = "Скажи, пожалуйста, если хочешь узнать больше."
    if age <= 7:
        tip = "Если хочешь, я расскажу ещё простыми словами!"

    return f"{base}Давай подумаем вместе: {question.strip()} {tip}"


