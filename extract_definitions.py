import re
import os
import pandas as pd
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
def extract_definitions(text):
    """Extracts definitions from a text string, handling numbered lists and multi-line definitions.

    Args:
        text: The text string to process.

    Returns:
        A dictionary where keys are terms and values are their definitions.
    """
    definitions = {}
    # Regex to find definitions, handling multi-line definitions and numbered lists

    patterns = [
        r'"([^"]+)" means,(.+?)(?=\n"|\Z)',
        r'"([^"]+)"\s+means(?:(?:\s*:\s*)|(?:\s+is\s+)|(?:\s+has\s+the\s+meaning\s+given\s+to\s+that\s+term\s+in\s+)|(?:\s+means\s+)|(?:\s+shall\s+mean\s+))((?:(?!\n\n).)*)',
        r'"([^"]+)"\s+means\s*((?:\((?:[a-z]+)\)\s+)?(?:(?!\n\n).)*)'
    ]
    master_matches = []
    for pattern in patterns:
        definition_pattern = re.compile(pattern, re.DOTALL)
        matches = definition_pattern.findall(text)
        master_matches.extend(matches)
    return master_matches
    # for term, definition in master_matches:
    #     cleaned_term = term.strip()
    #     cleaned_definition = definition.strip().replace('\n', ' ')
    #     definitions[cleaned_term] = cleaned_definition
    # return definitions
def debt_service_flag(name_file,debt_service_exist ):
    if len(debt_service_exist)>0:
        debt_service_term= True
        section_found_master = []
        source_text_master = []
        for item in debt_service_exist:
            # print(item[0])
            section_found = item[0]
            section_found_master.append(section_found)
            # extract out ebitda term only
            test2 = 'ADJUSTED EBITDA' + item[1].upper().split('ADJUSTED EBITDA')[1]
            # debt_service_exist[0]
            source_text = test2.split('\n\n')[0]
            source_text_master.append(section_found + '\n\n' + source_text)
        d = {'document_name': [name_file], 'term_name': ['debt_service_Flag'],'term_value': [debt_service_term],'term_section_found': [', '.join(section_found_master)],'term_source': ['-----------'.join(source_text_master)]}
        df = pd.DataFrame(data=d)
    else:
        debt_service_term=False
        d = {'document_name': [name_file], 'term_name': ['debt_service_Flag'],'term_value': [debt_service_term],'term_section_found': [None],'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df

master_df = pd.DataFrame()
test_lsit = []
for file_name in os.listdir('./markdown/'):
    # print(file_name)
    with open(f'./markdown/{file_name}', 'r', encoding="utf-8") as file:
        text = file.read()
        text = text.replace("**", "").replace("**", "").replace("“",'"').replace("”",'"')

    sections = extract_headers_and_content(text, main_section_extract=False)
    # Adjusted Ebitda:
    financial_cov = [x for x in sections if ('DEFINITIONS' in x[0].upper())]
    # leveragetemp = [x for x in sections if 'EQUITY CURE' in x[0].upper()]
    temp_text = '\n\n'.join([x[1] for x in financial_cov])
    if file_name=='dla_piper.md':
        print(temp_text)
    temp_matches = extract_definitions(temp_text)
    debt_service = [x for x in temp_matches if 'DEBT SERVICE' in x[0].upper()]
    test_lsit.append((file_name,debt_service))
    # master_df = pd.concat([master_df,temp_df1])
# text='\n\n'.join([x[1] for x in subsections]).replace("**", "").replace("“",'"').replace("”",'"')
#
# definitions = {}
#
# patterns = [
#     r'"([^"]+)"\s+means(?:(?:\s*:\s*)|(?:\s+is\s+)|(?:\s+has\s+the\s+meaning\s+given\s+to\s+that\s+term\s+in\s+)|(?:\s+means\s+)|(?:\s+shall\s+mean\s+))((?:(?!\n\n).)*)',
#      r'"([^"]+)"\s+means\s*((?:\((?:[a-z]+)\)\s+)?(?:(?!\n\n).)*)'
# ]
# master_matches = []
# for pattern in patterns:
#     definition_pattern = re.compile(pattern, re.DOTALL)
#     matches = definition_pattern.findall(text)
#     master_matches.extend(matches)
#
#
# test = [x for x in master_matches if 'DEBT SERVICE' in x[0].upper()]
# # Regex to find definitions, handling multi-line definitions
# definition_pattern = re.compile(
#    r'"([^"]+)"\s+means(?:(?:\s*:\s*)|(?:\s+is\s+)|(?:\s+has\s+the\s+meaning\s+given\s+to\s+that\s+term\s+in\s+)|(?:\s+means\s+)|(?:\s+shall\s+mean\s+))((?:(?!\n\n).)*)',
#     re.DOTALL
# )
#
