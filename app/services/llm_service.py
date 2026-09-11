from openai import OpenAI

from app.config import settings


def build_system_prompt() -> str:
    return """
You are an expert software estimator. Estimate implementation effort from meeting transcriptions.
Return a concise breakdown with assumptions, tasks, and total estimated hours.
"""


def build_user_message(transcription: str) -> dict[str, str]:
    return {"role": "user", "content": transcription}


def send_to_llm(system_prompt: str, user_message: dict[str, str]) -> dict[str, str]:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            user_message,
        ],
    )
    values: dict[str, str] = dict()

    values["total_tokens"]= str(response.usage.total_tokens);
    values["cost"]=str(response.usage.total_tokens/1000);
    values["cost_estimated"] = "$"+values["cost"];
    values["message"]=response.choices[0].message.content or ""

    return values

def estimate_duration(transcription: str) -> dict[str, str]:
    return send_to_llm(build_system_prompt(), build_user_message(transcription))
