# Resume Tailor

Resume Tailor is a simple website built using the Django MVT architecture. It allows you to upload a job description for a position you are applying for, along with your resume in PDF format.

The application will then tailor your resume based on the job description with high accuracy. From this tailored information, it builds an ATS-friendly LaTeX resume, allows you to preview it, and then lets you download the final version.

---

## Table of Contents
* [Current Features](#current-features)
* [Video Demo](#video-demo)
* [How It Works](#how-it-works)
* [Roadmap & Future Features](#roadmap--future-features)

---

## Current Features

* **File Upload:** Upload both the job description and your resume in PDF format.
* **Input Validation:** Validates the uploaded files to ensure they are in the correct format.
* **AI-Powered Tailoring:** Integrates with the Gemini API to parse your resume and tailor the content based on the provided job description.
* **Response Handling:** Validates and sanitizes the LLM's JSON response to ensure data integrity and security.
* **LaTeX Generation:** Dynamically builds an ATS-friendly LaTeX resume using the tailored information.
* **PDF Compilation:** Compiles the LaTeX source into a polished PDF document on the server.
* **Live Preview:** Allows you to preview the generated PDF resume directly in the browser.
* **Smart Download:** Lets you download the final resume with an automatic, context-aware filename: `YOUR_NAME_JOB_TITLE.pdf`.

---

## Video Demo

https://github.com/user-attachments/assets/581e671d-5e4b-4d19-a4c8-ded70d6cce1e

---

## How It Works

<img width="1321" height="1172" alt="Application Flow Diagram" src="https://github.com/user-attachments/assets/ed39adbb-2772-4c29-bfda-f9ab4d2e5424" />

---

## Roadmap & Future Features

I will be actively working on making Resume Tailor more robust and feature-rich. Here is a glimpse of what's coming next:

### Architecture & UI
- [ ] **REST API Transition:** Refactor core functionalities into a well-designed, scalable REST API.
- [ ] **Modern UI:** Develop a sleek, modern user interface to interact with the new API.
- [ ] **UX Enhancements:** Introduction of three major upcoming features designed to significantly improve the user experience.

### AI & Core Logic Improvements
- [ ] **Prompt Optimization:** Further refine LLM prompts to achieve even higher accuracy when tailoring content to job descriptions.
- [ ] **Robust Sanitization:** Implement advanced sanitization for all LLM responses to rigorously escape special characters, ensuring 100% reliable LaTeX compilation.
- [ ] **Enhanced Validation:** Comprehensive validation and error handling for all user inputs to improve application stability.

### Resume Template Enhancements
- [ ] **Dynamic Sections:** Support for optional and custom sections (e.g., Professional Summary, Certifications) via refactored Pydantic models and dynamic Jinja2 templates.
- [ ] **Smarter Personal Details:**
    - [ ] Accurate control over the number of allowed hyperlinks.
    - [ ] Cleaner display of social accounts (e.g., showing `@username` instead of raw GitHub/LinkedIn URLs).
- [ ] **Enriched Experience Section:** Add support for "Work Type" fields and optional hyperlinks for companies or specific projects.
- [ ] **Layout Integrity Control:** Automated constraints on hyperlink counts and description lengths for Projects and other sections to ensure perfectly structured PDF output every time.
