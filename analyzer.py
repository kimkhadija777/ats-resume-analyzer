import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from groq import Groq

from prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    build_analysis_prompt,
    get_response_schema,
)


load_dotenv()


def get_groq_client() -> Groq:
    """Create and return a Groq client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Create a .env file and add your Groq API key."
        )

    return Groq(api_key=api_key)


def validate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the most important fields in the AI response."""

    required_fields = [
        "match_score",
        "matching_skills",
        "missing_skills",
        "ats_keywords",
        "problems",
        "recommendations",
        "experience_match",
        "education_match",
        "final_result",
    ]

    for field in required_fields:

        if field not in result:
            raise ValueError(
                f"AI response is missing required field: {field}"
            )

    score = result["match_score"]

    if not isinstance(score, (int, float)):
        raise ValueError(
            "match_score must be a number."
        )

    if not 0 <= score <= 100:
        raise ValueError(
            "match_score must be between 0 and 100."
        )

    return result


def analyze_resume(
    resume_text: str,
    job_description: str,
    model: str,
) -> Dict[str, Any]:
    """
    Analyze a resume against a job description using Groq.
    """

    client = get_groq_client()

    user_prompt = build_analysis_prompt(
        resume_text=resume_text,
        job_description=job_description,
    )

    response_schema = get_response_schema()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": ANALYSIS_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_completion_tokens=5000,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_analysis",
                "strict": True,
                "schema": response_schema,
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "Groq returned an empty response."
        )

    try:
        result = json.loads(content)

    except json.JSONDecodeError as error:

        raise ValueError(
            "Groq returned invalid JSON."
        ) from error

    return validate_result(result)
