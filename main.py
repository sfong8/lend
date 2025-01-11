import PyPDF2
import re

def extract_sections(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = min(100, len(reader.pages))
        section_text = {}

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Regular expression to match section and sub-section headings
            section_pattern =  re.compile(r'^\d+\.\s+.*?(?=\n\d+\.\s|\$)', re.MULTILINE)
            sub_section_pattern = re.compile(r"\d+\.\d+\s+[A-Z\s$$]+\n")

            # Extract section and sub-section headings
            sections = section_pattern.findall(text)
            sub_sections = sub_section_pattern.findall(text)

            for section in sections:
                section_number = section.split()[0]
                section_text[section_number] = section

            for sub_section in sub_sections:
                sub_section_number = sub_section.split()[0]
                section_text[sub_section_number] = sub_section

            # Extract text following each section and sub-section
            current_section = None
            lines = text.split("\n")
            for line in lines:
                if re.match(section_pattern, line):
                    current_section = line.split()[0]
                    section_text[current_section] = ""
                elif re.match(sub_section_pattern, line):
                    current_section = line.split()[0]
                    section_text[current_section] = ""
                elif current_section:
                    section_text[current_section] += line + "\n"

            # Remove the heading from the text
            for key in section_text:
                section_text[key] = section_text[key].replace(key + " ", "", 1).strip()

    return section_text

# Example usage
pdf_path = "senior-facilities-agreement.pdf"  # Replace with your input PDF file path

section_text = extract_sections(pdf_path)

print("Sections extracted and stored in dictionary")
for section, text in section_text.items():
    print(f"Section {section}:\n{text}\n")