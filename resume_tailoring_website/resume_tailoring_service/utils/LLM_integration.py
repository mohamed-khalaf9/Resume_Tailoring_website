import json
import textwrap

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from .resume_content_pydantic_models import *


def construct_prompt(resume_content: str, hyper_links: list, job_description: str) -> str:

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

    1.  **Parse and Populate:** Read the `RESUME TEXT` and fill the JSON schema.
        * **`personal_info.accounts`:** Use the `HYPERLINK DATA` to find social/professional links. The `platform` should be the common name (e.g., "LinkedIn", "GitHub"). The `link` is the full URL.
        * **`projects.links`:** Use the `HYPERLINK DATA`. The `link` is the full URL. For the `description`, use the hyperlink's anchor text (e.g., "GitHub Repo", "Live Demo"). If no anchor text is available, use a logical default like "Source Code" or "Project Link".
        * **`additional_sections.items.link`:** Use the `HYPERLINK DATA` if a relevant link is found for an item (e.g., a certificate).
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

    4.  **Skills Grouping:** In the `skills` section, intelligently group all skills from the resume. Create meaningful `group_name` values (e.g., "Backend", "AI/ML", "Cloud & DevOps", "Databases", "Languages"(like english arabic and so on)).
        * **NEW RULE (Skill Tailoring):**
            1.  **Extract:** Identify all skills from the `RESUME TEXT`. Extract both the specific technology (e.g., "trie-based autocomplete") and the general concept it implies (e.g., "Data Structures", "Algorithms").
            2.  **Align & Report:** In the final `skills` JSON, prioritize listing the skills that are **both** supported by the resume and **explicitly mentioned** in the `JOB DESCRIPTION`. If the job description asks for "Data Structures," list that. If it *specifically* asks for "Trie algorithms," list that (since the resume provides evidence for it).

    5.  **Job Title:** Populate the `personal_info.job_required_title` field using the main job title found in the `JOB DESCRIPTION`. Do not use a title from the resume or guess a general one.

    ---
    ### 3. OUTPUT FORMAT
    ---

    You MUST return **ONLY** the raw JSON object, and nothing else. No introductions, no "Here is the JSON...". The output must be a single, valid JSON that strictly adheres to the schema provided below.

    **CRITICAL: LaTeX-Safe String Values**
    All string *values* within the JSON output **must** be sanitized for a LaTeX template.
    * Replace all underscore characters (`_`) with an escaped underscore (`\_`).
    * Remove or rephrase text to avoid special LaTeX characters like `&`, `%`, `$`, `#`, `{{`, `}}`.
    * Remove or replace single quotes (`'`) and double quotes (`"`) from within strings to prevent compilation errors. For example, rewrite "O'Brien" as "OBrien".

    **SCHEMA:**
    ```json
    {{
      "personal_info": {{
        "name": "string | "" ",
        "job_required_title": "string | "" ",
        "country": "string | "" ",
        "city": "string | "" ",
        "mobile_number": "string | "" ",
        "email": "string | "" ",
        "accounts": [
          {{
            "platform": "string | null",
            "link": "string | null"
          }}
        ] | []
      }},
      "education": [
        {{
          "university_name": "string | "" ",
          "degree": "string | "" ",
          "specialization": "string | "" ",
          "faculty": "string | "" ",
          "country": "string | "" ",
          "city": "string | "" ",
          "start_date": "string | "" ",
          "end_date": "string | "" ",
          "related_coursework": [
            "string | "" "
          ] | []
        }}
      ] | [],
      "experience": [
        {{
          "title": "string | "" ",
          "company_name": "string | "" ",
          "start_date": "string | "" ",
          "end_date": "string | "" ",
          "work_type": "string | "" ",
          "location": "string | "" ",
          "description": [
            "string | "" "
          ] | []
        }}
      ] | [],
      "projects": [
        {{
          "name": "string | "" ",
          "links": [
            {{
              "description": "string | "" ",
              "link": "string | "" "
            }}
          ] | [],
          "start_date": "string | "" ",
          "end_date": "string | "" ",
          "description": [
            "string | "" "
          ] | []
        }}
      ] | [],
      "skills": [
        {{
          "group_name": "string | "" ",
          "skills": [
            "string | "" "
          ] | []
        }}
      ] | [],
      "additional_sections": [
        {{
          "section_title": "string | "" ",
          "items": [
            {{
              "name": "string | "" ",
              "start_date": "string | "" ",
              "end_date": "string | "" ",
              "link": "string | "" ",
              "description": [
                "string | "" "
              ] | []
            }}
          ] | []
        }}
      ] | []
    }}
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


