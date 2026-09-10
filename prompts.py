ANALYSIS_SYSTEM_PROMPT = """
You are an expert AI Resume Analyzer.

Your task is to compare a candidate's resume with a specific job
description.

Analyze only the information provided in the resume and job description.

Do not invent skills, experience, education, certifications, projects,
or achievements.

If something is not clearly demonstrated in the resume, treat it as
missing or unclear.

Important rules:

1. Identify skills that genuinely match the job requirements.
2. Identify important skills that are missing from the resume.
3. Identify important ATS keywords from the job description.
4. Mark each keyword as found, partial, or missing.
5. Identify genuine resume problems relevant to this job.
6. Provide practical recommendations.
7. Evaluate experience and education requirements.
8. Produce a realistic match score from 0 to 100.
9. The score must reflect the overall alignment between the resume
   and job description.
10. Do not tell the candidate to falsely claim skills or experience.
11. Do not treat every keyword as equally important.
12. Distinguish between required and preferred requirements when possible.
13. Return ONLY the requested JSON structure.
"""


def build_analysis_prompt(
    resume_text: str,
    job_description: str,
) -> str:
    """Build the user prompt for the AI model."""

    return f"""
Analyze the following resume against the following job description.

====================
RESUME
====================

{resume_text}

====================
JOB DESCRIPTION
====================

{job_description}

====================
TASK
====================

Compare the resume with the job description.

Return:

- Overall match score
- Matching skills
- Missing skills
- Important ATS keywords
- Resume problems
- Recommendations
- Experience match
- Education match
- Final result

Remember:

Only use information provided in the resume.

Do not invent candidate information.
"""


def get_response_schema() -> dict:
    """Return the JSON schema expected from the AI."""

    return {
        "type": "object",
        "properties": {

            "match_score": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
            },

            "matching_skills": {
                "type": "array",
                "items": {
                    "type": "string"
                },
            },

            "missing_skills": {
                "type": "array",
                "items": {
                    "type": "string"
                },
            },

            "ats_keywords": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {

                        "keyword": {
                            "type": "string"
                        },

                        "status": {
                            "type": "string",
                            "enum": [
                                "found",
                                "partial",
                                "missing",
                            ],
                        },

                    },
                    "required": [
                        "keyword",
                        "status",
                    ],
                    "additionalProperties": False,
                },
            },

            "problems": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {

                        "problem": {
                            "type": "string"
                        },

                        "explanation": {
                            "type": "string"
                        },

                    },
                    "required": [
                        "problem",
                        "explanation",
                    ],
                    "additionalProperties": False,
                },
            },

            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {

                        "recommendation": {
                            "type": "string"
                        },

                        "reason": {
                            "type": "string"
                        },

                    },
                    "required": [
                        "recommendation",
                        "reason",
                    ],
                    "additionalProperties": False,
                },
            },

            "experience_match": {
                "type": "object",
                "properties": {

                    "status": {
                        "type": "string",
                        "enum": [
                            "strong",
                            "moderate",
                            "weak",
                            "unclear",
                            "not_required",
                        ],
                    },

                    "explanation": {
                        "type": "string"
                    },

                },
                "required": [
                    "status",
                    "explanation",
                ],
                "additionalProperties": False,
            },

            "education_match": {
                "type": "object",
                "properties": {

                    "status": {
                        "type": "string",
                        "enum": [
                            "strong",
                            "moderate",
                            "weak",
                            "unclear",
                            "not_required",
                        ],
                    },

                    "explanation": {
                        "type": "string"
                    },

                },
                "required": [
                    "status",
                    "explanation",
                ],
                "additionalProperties": False,
            },

            "final_result": {
                "type": "object",
                "properties": {

                    "label": {
                        "type": "string",
                        "enum": [
                            "Strong Match",
                            "Moderate Match",
                            "Weak Match",
                        ],
                    },

                    "summary": {
                        "type": "string"
                    },

                },
                "required": [
                    "label",
                    "summary",
                ],
                "additionalProperties": False,
            },

        },

        "required": [
            "match_score",
            "matching_skills",
            "missing_skills",
            "ats_keywords",
            "problems",
            "recommendations",
            "experience_match",
            "education_match",
            "final_result",
        ],

        "additionalProperties": False,
  }
