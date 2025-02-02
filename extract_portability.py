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

#sub section extraction
def equity_cure_flag(name_file,equity_cure_exist ):
    if len(equity_cure_exist)>0:
        equity_cure_term= True
        section_found_master = []
        source_text_master = []
        for item in equity_cure_exist:
            # print(item[0])
            section_found = item[0]
            section_found_master.append(section_found)
            # extract out ebitda term only
            if 'EQUITY CURE' in section_found.upper():
                source_text = item[1]
            else:
                test2 = 'EQUITY CURE' + item[1].upper().split('EQUITY CURE')[1]
            # equity_cure_exist[0]
                source_text = test2.split('\n\n')[0]
            source_text_master.append(section_found + '\n\n' + source_text)
        d = {'document_name': [name_file], 'term_name': ['equity_cure_Flag'],'term_value': [equity_cure_term],'term_section_found': [', '.join(section_found_master)],'term_source': ['-----------'.join(source_text_master)]}
        df = pd.DataFrame(data=d)
    else:
        equity_cure_term=False
        d = {'document_name': [name_file], 'term_name': ['equity_cure_Flag'],'term_value': [equity_cure_term],'term_section_found': [None],'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df


sections = extract_headers_and_content(text, main_section_extract=True)
#Adjusted Ebitda:
mandatory_payments = [x for x in sections if ('MANDATORY PREPAYMENT' in x[0].upper()) or ('DEFINITIONS' in x[0].upper())or ('EVENTS OF DEFAULT' in x[0].upper())]
# equity_cure_temp = [x for x in sections if 'EQUITY CURE' in x[0].upper()]
subsections = []

for section_text in mandatory_payments:
    temp_sections = extract_headers_and_content(section_text[1], main_section_extract=False)
    subsections.extend(temp_sections)

# financial_definitions.extend((equity_cure_temp))

#check if adjusted ebitda term is in it
change_of_control = [x for x in subsections if "CHANGE OF CONTROL" in x[1].upper()]

subsections2 = extract_headers_and_content(text, main_section_extract=False)
change_of_control2 = [x for x in subsections2 if "CHANGE OF CONTROL" in x[1].upper()]
#
#
# master_df = pd.DataFrame()
# for file_name in os.listdir('./markdown/'):
#     # print(file_name)
#     with open(f'./markdown/{file_name}', 'r', encoding="utf-8") as file:
#         text = file.read()
#         text = text.replace("**", "")
#     sections = extract_headers_and_content(text, main_section_extract=False)
#     # Adjusted Ebitda:
#     financial_definitions = [x for x in sections if 'DEFINITIONS' in x[0].upper()]
#     equity_cure_temp = [x for x in sections if 'EQUITY CURE' in x[0].upper()]
#     financial_definitions.extend((equity_cure_temp))
#     # check if adjusted ebitda term is in it
#     equity_cure = [x for x in financial_definitions if "EQUITY CURE" in x[1].upper()]
#     temp_df1 = equity_cure_flag(file_name,equity_cure)
#     master_df = pd.concat([master_df,temp_df1])