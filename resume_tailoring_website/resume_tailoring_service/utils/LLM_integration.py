import json
import textwrap

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from .resume_content_pydantic_models import *


def construct_prompt(resume_content: str, hyper_links: list, job_description: str) -> str:
    """
    Constructs the prompt for the Gemini API with detailed instructions
    for parsing, tailoring, and rewriting a resume.

    Args:
        resume_content: The full unstructured text of the resume.
        hyper_links: A list of dicts containing hyperlink data.
        job_description: The full text of the target job description.

    Returns:
        A formatted prompt string.
    """

    # Serialize the list of hyperlink objects into a JSON string.
    hyper_links_str = json.dumps(hyper_links)

    # Use textwrap.dedent to remove the leading whitespace from the
    # multi-line f-string.
    # All { and } in the JSON schema MUST be escaped as {{ and }}
    # so the f-string doesn't interpret them as variables.

    prompt = textwrap.dedent(f"""
    You are an expert technical resume parser and career-coaching assistant. Your sole task is to:
    1.  Parse an unstructured resume and its associated hyperlink data.
    2.  Analyze a target job description.
    3.  Tailor the resume content to align with the job description, using *only* information present in the original resume.
    4.  Rewrite experience and project descriptions to be impact-oriented *only if* impact is clearly stated.
    5.  Return a single, valid JSON object matching a precise schema.

    ---
    ### 1. INPUT DATA
    ---

    Here is the unstructured resume text, hyperlink data, and the target job description.

    **--- RESUME TEXT ---**
    {resume_content}
    ---

    **--- HYPERLINK DATA ---**
    {hyper_links_str}
    ---

    **--- JOB DESCRIPTION ---**
    {job_description}
    ---

    ---
    ### 2. CORE INSTRUCTIONS
    ---

    **GUIDING PRINCIPLE:** Your primary goal is **accuracy and truthfulness**. You are a parser and a *light* copy-editor, not a creative writer. Do not add *any* information, numbers, or metrics not explicitly present in the `RESUME TEXT`. It is **better to have a simple, truthful bullet point** than an exaggerated, impact-oriented one that is a lie.

    1.  **Parse and Populate:** Read the `RESUME TEXT` and fill the JSON schema. Use the `HYPERLINK DATA` to correctly populate all link-related fields (e.g., `personal_info.accounts`, `projects.links`, `additional_sections.items.link`).
        * **NEW RULE (Education):** Be granular and intelligent when parsing education.
            * **Example 1:** If text is "Bachelor of Science in Information Technology", you MUST set: `degree: "Bachelor"`, `faculty: "Science"`, `specialization: "Information Technology"`.
            * **Example 2:** If text is "Bachelor of Science", you MUST set: `degree: "Bachelor"`, `faculty: "Science"`.
            * **Example 3:** If text is "Bachelor, Computer Science", you MUST set: `degree: "Bachelor"`, `specialization: "Computer Science"`.
            * Always try to split the degree level (Bachelor, Master) from the faculty (Science, Arts, Engineering) and the specialization (Computer Science, Information Technology).

    2.  **Tailor (No Hallucination):** Analyze the `JOB DESCRIPTION`. Identify key skills, technologies, and responsibilities.
        * **CRITICAL:** You must *only* use information, skills, and experiences found in the original `RESUME TEXT`.
        * **DO NOT** invent new facts, skills, or experiences, even if they are in the job description.
        * Your goal is to *re-frame and emphasize* the candidate's existing qualifications that match the job. If the candidate lacks a skill from the job description, simply omit it.

    3.  **Rewrite for Impact (If Possible):** For all `description` fields (in `experience`, `projects`, and `additional_sections`), review the bullet points.
        * **If** the original bullet point provides a quantifiable result or clear impact (a metric, number, or clear outcome [Y]), **then** rewrite it to follow the "Accomplished [X] as measured by [Y] by doing [Z]" format.
        * **Example (if impact is present):** If the resume says "Wrote APIs that improved login speed by 20%", you should rewrite it as: "Improved login speed by 20% [Y] by developing new REST APIs [Z] for the user-auth module [X]."
        * **CRITICAL CAVEAT:** If the original bullet point is a simple responsibility (e.g., "Wrote APIs," "Managed databases") and **no impact or metric [Y] is mentioned**, **DO NOT INVENT ONE.** Simply transfer the cleaned-up responsibility (e.g., "Developed and maintained REST APIs for backend services.")
        * **NEW RULE (Be Intelligent):** Do not be a robot. If a bullet point is *already* well-written and clear, you do not need to forcibly rewrite it. Only apply the X-Y-Z format if it genuinely adds value *and* all parts (X, Y, Z) are present.

    4.  **Skills Grouping:** In the `skills` section, intelligently group all skills from the resume. Create meaningful `group_name` values (e.g., "Backend", "AI/ML", "Cloud & DevOps", "Databases").
        * **NEW RULE (Skill Generality):** Extract skills at a reasonable level of generality. For example, if a project mentions 'trie-based autocomplete', the extracted skill should be 'Algorithms' or 'Data Structures', **not** the hyper-specific 'Trie-based algorithms'. Use your judgment to list skills the candidate likely possesses *based on the evidence*, without being overly restrictive.

    5.  **Job Title:** Populate the `personal_info.job_required_title` field using the main job title from the `JOB DESCRIPTION`.

    ---
    ### 3. OUTPUT FORMAT
    ---

    You MUST return **ONLY** the raw JSON object, and nothing else. No introductions, no "Here is the JSON...". The output must be a single, valid JSON that strictly adheres to the schema provided below.

    **SCHEMA:**
    ```json
    {{
      "personal_info": {{
        "name": "string | null",
        "job_required_title": "string | null",
        "country": "string | null",
        "city": "string | null",
        "mobile_number": "string | null",
        "email": "string | null",
        "accounts": [
          {{
            "platform": "string | null",
            "link": "string | null"
          }} | null
        ] | null
      }} | null,
      "education": [
        {{
          "university_name": "string | null",
          "degree": "string | null",
          "specialization": "string | null",
          "faculty": "string | null",
          "country": "string | null",
          "city": "string | null",
          "start_date": "string | null",
          "end_date": "string | null",
          "related_coursework": [
            "string | null"
          ] | null
        }} | null
      ] | null,
      "experience": [
        {{
          "title": "string | null",
          "company_name": "string | null",
          "start_date": "string | null",
          "end_date": "string | null",
          "work_type": "string | null",
          "location": "string | null",
          "description": [
            "string | null"
          ] | null
        }} | null
      ] | null,
      "projects": [
        {{
          "name": "string | null",
          "links": [
            {{
              "description": "string | null",
              "link": "string |null"
            }} | null
          ] | null,
          "start_date": "string | null",
          "end_date": "string | null",
          "description": [
            "string | null"
          ] | null
        }} | null
      ] | null,
      "skills": [
        {{
          "group_name": "string | null",
          "skills": [
            "string | null"
          ] | null
        }} | null
      ] | null,
      "additional_sections": [
        {{
          "section_title": "string | null",
          "items": [
            {{
              "name": "string | null",
              "start_date": "string | null",
              "end_date": "string | null",
              "link": "string | null",
              "description": [
                "string | null"
              ] | null
            }} | null
          ] | null
        }} | null
      ] | null
    }}
    ```
    """)

    return prompt




def tailor_resume(resume_content: str, hyperlinks:list, job_description:str):
    raw_text = None
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found in environment.")
            return None

        prompt = construct_prompt(resume_content, hyperlinks, job_description)

        client = genai.Client(api_key=api_key)

        model = "gemini-2.5-flash"

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents,
        )

        raw_text = response.text

        cleaned_text = raw_text.strip().removeprefix("```json").removesuffix("```").strip()

        if not cleaned_text:
            print("Error: API returned an empty response.")
            return None

        json_response = json.loads(cleaned_text)
        pydantic_resume = ResumeContent.model_validate(json_response)

        return pydantic_resume

    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode API response into JSON. Error: {e}")
        if raw_text:
            print(f"--- Raw response text from API ---")
            print(raw_text)
            print("-----------------------------------")
        return None
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None


