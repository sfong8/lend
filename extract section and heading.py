import re
name_file = 'Amalfi_-_SFA_dated_27_Jun_2022.md'
with open(f'./markdown/{name_file}', 'r', encoding="utf-8") as file:
    text = file.read()
def extract_headers_and_content(text, main_section_extract=True):
    """
    Extracts headers and their corresponding content from a given text.

    Args:
        text (str): The input text containing headers and content.
        main_section_extract (bool, optional): If True, extracts only the main sections (e.g., 1. Definitions)
                                             instead of individual subsections (e.g., 1.1 Definition, etc.).
                                             Defaults to True.

    Returns:
        list: A list of tuples, where each tuple contains the header and its corresponding content.
    """

    if main_section_extract:
        pattern = r'(\*\*\d+\.\*\*\s*\*\*[^*]+\*\*)\s*(.*?)(?=\n\*\*\d+\.|\Z)'
    else:
        pattern = r'(\*\*\d+\.(?:\d+)?\*\*\s*\*\*[^*]+\*\*)\s*(.*?)(?=\n\*\*\d+\.|\Z)'

    matches = re.findall(pattern, text, re.DOTALL)

    if len(matches) == 0:
        if main_section_extract:
            section_pattern = re.compile(r'^(\d+\.\s+[A-Z\s-]+)', re.MULTILINE)
        else:
            section_pattern = re.compile(r'(\d+\.\d+\s+[A-Z].*)', re.MULTILINE)

        sections = section_pattern.findall(text)
        matches = [(section, "") for section in sections]

        # Extract text between sections
        section_texts = []
        last_section = None
        last_index = 0

        for match in section_pattern.finditer(text):
            section = match.group(1)
            start_index = match.start()

            if last_section:
                section_texts.append((last_section, text[last_index:start_index].strip()))

            last_section = section
            last_index = start_index

        if last_section:
            # section_texts[last_section] = text[last_index:].strip()
            section_texts.append((last_section, text[last_index:].strip()))
        return section_texts
        # Process and return the results
    else:
        results = []
        for header, content in matches:
            # Remove asterisks and extra spaces from the header
            clean_header = re.sub(r'\*+', '', header).strip()

            # Remove Leading/trailing whitespace and newlines from content
            clean_content = content.strip()

            results.append((clean_header, clean_content))

        return results

# Example usage:

extracted_sections = extract_headers_and_content(text)
print(extracted_sections)

# Add the text after the last section
section_pattern = re.compile(r'^(\d+\.\s+[A-Z\s–]+)', re.MULTILINE)
# Find all matches
sections = section_pattern.findall(text)

extracted_data = extract_headers_and_content(text, main_section_extract=True)
extracted_data2 = extract_headers_and_content(text, main_section_extract=False)

# Print the extracted headers and content
for header, content in extracted_data:
    print(f"Header: {header}")
    print(f"Content: {content}")
    print()

financial_covenant_dict = [x for x in extracted_data2 if "26." in x[0].upper()]

# focus on the financial covenant section first
financial_covenant_text = [x for x in extracted_data if "FINANCIAL COVENANT" in x.upper()]

# we then split it down in subsections
financial_covenant_subsection = extract_headers_and_content(financial_covenant_text, main_section_extract=False)

