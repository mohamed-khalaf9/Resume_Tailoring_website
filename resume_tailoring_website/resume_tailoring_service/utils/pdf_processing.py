import fitz

def extract_resume_content(resume_pdf_file):
    resume = fitz.open(stream=resume_pdf_file,filetype="pdf")
    resume_content = ""
    all_links_details = []
    for page in resume:
        resume_content += page.get_text() + "\n"
        links = page.get_links()


        for link in links:
            link_details = {
                "page_number": page.number + 1,
                "text": None,
                "hyperlink": None,
                "type": None,
            }
            # extract URI
            uri = link.get("uri")
            rect = link.get("from", None)
            if rect:
                link_details["text"] = page.get_textbox(rect).strip() if page.get_textbox(rect) else "(No text)"

            if uri:
                link_details["type"] = "URI"
                link_details["hyperlink"] = uri
            else:
                # Check if it's a different type of link
                if "type" in link:
                    link_details["type"] = link["type"]
                else:
                    link_details["type"] = "Unrecognized or custom action"

            all_links_details.append(link_details)

    return all_links_details,resume_content