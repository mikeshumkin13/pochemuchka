from app.services.llm import _build_system_prompt

def test_prompt_5_7():
    p = _build_system_prompt(6)
    assert "5–7" in p and "2–3 коротких предложения" in p

def test_prompt_8_11():
    p = _build_system_prompt(10)
    assert "8–11" in p and "3–5 предложений" in p

def test_prompt_12_15():
    p = _build_system_prompt(14)
    assert "12–15" in p and "2–3 пункта" in p

def test_prompt_16_17():
    p = _build_system_prompt(17)
    assert "16–17" in p and "«что это», «почему так», «пример»" in p


