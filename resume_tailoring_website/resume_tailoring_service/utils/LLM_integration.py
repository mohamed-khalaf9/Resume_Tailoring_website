import json
import textwrap

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


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

    1.  **Parse and Populate:** Read the `RESUME TEXT` and fill the JSON schema. Use the `HYPERLINK DATA` to correctly populate all link-related fields (e.g., `personal_info.accounts`, `projects.links`, `additional_sections.items.link`).
    2.  **Tailor (No Hallucination):** Analyze the `JOB DESCRIPTION`. Identify key skills, technologies, and responsibilities.
        * **CRITICAL:** You must *only* use information, skills, and experiences found in the original `RESUME TEXT`.
        * **DO NOT** invent new facts, skills, or experiences, even if they are in the job description.
        * Your goal is to *re-frame and emphasize* the candidate's existing qualifications that match the job. If the candidate lacks a skill from the job description, simply omit it.
    3.  **Rewrite for Impact (If Possible):** For all `description` fields (in `experience`, `projects`, and `additional_sections`), review the bullet points.
        * **If** the original bullet point provides a quantifiable result or clear impact (a metric, number, or clear outcome [Y]), **then** rewrite it to follow the "Accomplished [X] as measured by [Y] by doing [Z]" format.
        * **Example (if impact is present):** If the resume says "Wrote APIs that improved login speed by 20%", you should rewrite it as: "Improved login speed by 20% [Y] by developing new REST APIs [Z] for the user-auth module [X]."
        * **CRITICAL CAVEAT:** If the original bullet point is a simple responsibility (e.g., "Wrote APIs," "Managed databases") and **no impact or metric [Y] is mentioned**, **DO NOT INVENT ONE.** Simply transfer the cleaned-up responsibility (e.g., "Developed and maintained REST APIs for backend services.")
        * Your priority is to be truthful to the original text. Only apply the X-Y-Z format when the data supports it.
    4.  **Skills Grouping:** In the `skills` section, intelligently group all skills from the resume. Create meaningful `group_name` values (e.g., "Backend", "AI/ML", "Cloud & DevOps", "Databases").
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





def tailor_resume(resume_content: str, hyperlinks:list, job_description:str) -> dict | None:
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

        return json_response

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


