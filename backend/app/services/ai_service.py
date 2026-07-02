import json

from openai import OpenAI

from ..config import settings

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file.")
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["Strong Match", "Partial Match", "Needs Work"],
        },
        "summary": {"type": "string"},
        "missingSkills": {"type": "array", "items": {"type": "string"}},
        "suggestedKeywords": {"type": "array", "items": {"type": "string"}},
        "interviewTopics": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["verdict", "summary", "missingSkills", "suggestedKeywords", "interviewTopics"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are an exacting technical recruiter and resume coach. Compare the resume "
    "against the job description and report back factually, in plain language. "
    "Limit missingSkills to at most 8 items, suggestedKeywords to at most 10 items, "
    "and interviewTopics to at most 6 items. Keep summary to at most 2 sentences."
)


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Calls OpenAI's Responses API with a strict JSON schema and returns a plain dict.

    Structured Outputs guarantee the shape of the response, so no manual
    JSON-cleanup or regex extraction is needed on this end.
    """
    client = get_client()

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description}",
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "resume_report",
                "strict": True,
                "schema": REPORT_SCHEMA,
            }
        },
    )

    return json.loads(response.output_text)
