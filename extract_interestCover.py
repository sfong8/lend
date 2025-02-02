import os
import re
import pandas as pd
name_file = 'Amalfi_-_SFA_dated_27_Jun_2022.md'
# name_file = 'project_amalfi.md'
with open(f'./markdown/{name_file}', 'r', encoding="utf-8") as file:
    text = file.read()


import pandas as pd
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_cure_limit_pos(text):
    """
    Extracts the number of permitted equity cures from a given text using POS tagging.

    Args:
        text (str): The text of the loan agreement.

    Returns:
        int or None: The number of permitted cures, or None if not found.
    """
    text = re.sub(r'\b(' + '|'.join(text_to_number.keys()) + r')\b', text_to_numeric, text, flags=re.IGNORECASE)
    doc = nlp(text)
    cure_limit = None
    for token in doc:
        if token.pos_ == "NUM":
            # Check if the number is related to "times" or "cures"

            for child in token.children:
                # print(child)
                if child.text.lower() in ["times", "cures"]:
                    try:
                        cure_limit = int(token.text)
                        return cure_limit
                    except ValueError:
                        continue
            # Check if the number is related to "exercise"
            if token.head.text.lower() in ["exercise", "remedy"]:
                for child in token.head.children:
                    if child.text.lower() in ["times", "cures"]:
                        try:
                            cure_limit = int(token.text)
                            return cure_limit
                        except ValueError:
                            continue
    return cure_limit
# Mapping of textual numbers to numeric values
text_to_number = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
}

# Function to convert textual number to numeric
def text_to_numeric(match):
    return str(text_to_number.get(match.group(0).lower(), 0))
def extract_cure_limit(text):
    """
    Extracts the number of permitted equity cures from a given text.

    Args:
        text (str): The text of the loan agreement.

    Returns:
        int or None: The number of permitted cures, or None if not found.
    """
    patterns = [
        r"may only exercise its rights under paragraph \(a\) above:.*?(\d+)\s+times",
        r"may only remedy a curable event of default:.*?up to (\d+)\s+times",
        r"may only exercise its rights under paragraph \(a\) above:.*?(\d+)\s+times before the termination date"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower(), re.DOTALL)
        if match:
            return int(match.group(1))
    return None
# Function to extract the number of cures
def extract_number_of_cures(text):
    # Replace textual numbers with numeric values
    text = re.sub(r'\b(' + '|'.join(text_to_number.keys()) + r')\b', text_to_numeric, text, flags=re.IGNORECASE)
    # print(text)
    # Look for patterns that indicate the number of times a cure is allowed
    patterns = [
        r'up to (\d+) times',  # e.g., "up to four times"
        r'(\d+) times',  # e.g., "four times"
        r'not more than (\d+)',  # e.g., "not more than four"
        r'only (\d+) times'  # e.g., "only four times"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None

# Apply the function to the relevant column


# Display the results
def extract_headers_and_content(text, main_section_extract=True):
    """
    Extracts headers and their corresponding content from a given text.

    Args:
        text (str): The input text containing headers and content.
        main_section_extract (bool, optional): If True, extracts only the main sections (e.g., 1. Definitions)
                                             instead of individual subsections (e.g., 1.1 Definition, etc.).
                                             Defaults to True.

    Returns:
        list: A list of tuples, where each tuple contains the header and its corresponding content. as
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


def interCover_flag(file_name,subsections):
    # definitions
    definitions  =  [x for x in subsections if ('DEFINITIONS' in x[0].upper())]
    #breakdown the definitions into list
    leverageterm = False
    section_found_master = []
    source_text_master = []
    for item in definitions:
        definitions_list = item[1].split('\n\n')
        flat_list = [   x  for x in definitions_list if 'INTEREST COVER' in x[:20].upper()]
        if len(flat_list)>0:
            leverageterm = True
            section_found = item[0]
            section_found_master.append(section_found)
            source_text_master.append(section_found + '\n\n' + '\n'.join(flat_list))
    if leverageterm:
        d = {'document_name': [file_name], 'term_name': ['leverageFlag'], 'term_value': [leverageterm],
             'term_section_found': [', '.join(section_found_master)],
             'term_source': ['-----------'.join(flat_list)]}
        df = pd.DataFrame(data=d)
    else:
        d = {'document_name': [file_name], 'term_name': ['leverageFlag'], 'term_value': [leverageterm],
             'term_section_found': [None], 'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df

master_df = pd.DataFrame()
for file_name in os.listdir('./markdown/'):
    # print(file_name)
    with open(f'./markdown/{file_name}', 'r', encoding="utf-8") as file:
        text = file.read()
        text = text.replace("**", "")
    sections = extract_headers_and_content(text, main_section_extract=True)
    # Adjusted Ebitda:
    financial_cov = [x for x in sections if ('FINANCIAL COVENANTS' in x[0].upper()) or ('DEFINITIONS' in x[0].upper())]
    # leveragetemp = [x for x in sections if 'EQUITY CURE' in x[0].upper()]
    subsections = []

    for section_text in financial_cov:
        temp_sections = extract_headers_and_content(section_text[1], main_section_extract=False)
        subsections.extend(temp_sections)
    temp_df1 = interCover_flag(file_name,subsections)
    master_df = pd.concat([master_df,temp_df1])

master_df=master_df.reset_index()
# master_df['cure_limit'] = None
#
# for index, row in master_df.iterrows():
#     if row['term_value'] == True:
#         print(row['document_name'])
#         text = row['term_source']
#         cure_limit = extract_cure_limit(text)
#         master_df.loc[index, 'cure_limit'] = cure_limit
