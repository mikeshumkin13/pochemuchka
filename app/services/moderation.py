BAD_WORDS = {"насилие", "оружие", "наркотик"}

def is_safe(text: str) -> bool:
    low = text.lower()
    return not any(b in low for b in BAD_WORDS)


