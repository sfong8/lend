import os
import re
import pandas as pd
name_file = 'Amalfi_-_SFA_dated_27_Jun_2022.md'
# name_file = 'project_amalfi.md'
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

sections = extract_headers_and_content(text, main_section_extract=False)
#Adjusted Ebitda:
financial_definitions = [x for x in sections if 'DEFINITIONS' in x[0].upper()]

#check if adjusted ebitda term is in it
adjusted_ebitda_exist = [x for x in financial_definitions if "ADJUSTED EBITDA" in x[1].upper()]

def adjusted_ebitda_flag(name_file,adjusted_ebitda_exist ):
    if len(adjusted_ebitda_exist)>0:
        adjusted_ebitda_term= True
        section_found_master = []
        source_text_master = []
        for item in adjusted_ebitda_exist:
            # print(item[0])
            section_found = item[0]
            section_found_master.append(section_found)
            # extract out ebitda term only
            test2 = 'ADJUSTED EBITDA' + item[1].upper().split('ADJUSTED EBITDA')[1]
            # adjusted_ebitda_exist[0]
            source_text = test2.split('\n\n')[0]
            source_text_master.append(section_found + '\n\n' + source_text)
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Flag'],'term_value': [adjusted_ebitda_term],'term_section_found': [', '.join(section_found_master)],'term_source': ['-----------'.join(source_text_master)]}
        df = pd.DataFrame(data=d)
    else:
        adjusted_ebitda_term=False
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Flag'],'term_value': [adjusted_ebitda_term],'term_section_found': [None],'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df

def adjusted_ebidta_cap(name_file,adjusted_ebitda_exist):
    percent_master = []
    for item in adjusted_ebitda_exist:
        # print(item[0])
        section_found = item[0]
        # extract out ebitda term only
        test2 = 'ADJUSTED EBITDA' + item[1].upper().split('ADJUSTED EBITDA')[1]
        # adjusted_ebitda_exist[0]
        percent_cent = [x.replace("\n"," ")  for x in test2.split('\n\n') if ('PER CENT' in x.upper().replace("\n"," ") ) or ('PER. CENT' in x.upper().replace("\n"," ") )]
        # search for exceed as wel
        percent_master.extend(percent_cent)
    if len(percent_master):
        percent_master_text = ' '.join(percent_master)
        section_found_exceptional = section_found
        # get the percentage
        # Use a regular expression to find the percentage.  The \d+ matches one or more digits, the \s* matches zero or more whitespace characters, and the % matches the percent sign.
        # match = re.search(r'(\d+)\s*', percent_master_text)
        # Method 1: Using re.search() to find the whole phrase.
        match = re.search(r"SHALL NOT EXCEED \d+ PER CENT",
                          percent_master_text.upper())  # \d+ for one or more digits, \. to match the period.
        if match:
            found_text = match.group(0)  # Get the entire matched text
            match2 = re.search(r'(\d+)\s*', found_text)
            percentage = str(int(match2.group(1)))  # Extract the captured group (the number) and convert to integer
        else:
            percentage = 'N/A'
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Cap'], 'term_value': [percentage],
             'term_section_found': [section_found_exceptional],
             'term_source': [percent_master_text]}
        df = pd.DataFrame(data=d)
    else:
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Cap'],
             'term_value': [None],
             'term_section_found': [None],
             'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df
def exceptional_item_term(name_file,adjusted_ebitda_exist):
    exception_item_list_master= []
    for item in adjusted_ebitda_exist:
        # print(item[0])
        section_found = item[0]
        # extract out ebitda term only
        test2 = 'ADJUSTED EBITDA' + item[1].upper().split('ADJUSTED EBITDA')[1]
        # adjusted_ebitda_exist[0]
        exception_item_list = [x for x in test2.split('\n\n') if 'EXCEPTIONAL ITEM' in x.upper()]
        exception_item_list_master.extend(exception_item_list)
    if len(exception_item_list_master):
        exception_item_list_text = ' '.join(exception_item_list_master)
        section_found_exceptional = section_found
        exceptional_item_flag = 'No' if 'NO ' in  exception_item_list_text.upper() else 'Yes'
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Exceptional_Item_add_back'], 'term_value': [exceptional_item_flag],
             'term_section_found': [section_found_exceptional],
             'term_source': [exception_item_list_text]}
        df = pd.DataFrame(data=d)
    else:
        d = {'document_name': [name_file], 'term_name': ['Adjusted_EBITDA_Exceptional_Item_add_back'],
             'term_value': [None],
             'term_section_found': [None],
             'term_source': [None]}
        df = pd.DataFrame(data=d)
    return df
# create the master df
# adjusted ebidta exists
master_df = pd.DataFrame()
for file_name in os.listdir('./markdown/'):
    print(file_name)
    with open(f'./markdown/{file_name}', 'r', encoding="utf-8") as file:
        text = file.read()
        text = text.replace("**", "")
    sections = extract_headers_and_content(text, main_section_extract=False)
    # Adjusted Ebitda:
    financial_definitions = [x for x in sections if 'DEFINITIONS' in x[0].upper()]

    # check if adjusted ebitda term is in it
    adjusted_ebitda_exist = [x for x in financial_definitions if "ADJUSTED EBITDA" in x[1].upper()]
    temp_df1 = adjusted_ebitda_flag(file_name,adjusted_ebitda_exist)
    temp_df2 = exceptional_item_term(file_name,adjusted_ebitda_exist)
    temp_df3 = adjusted_ebidta_cap(file_name,adjusted_ebitda_exist)
    master_df = pd.concat([master_df,temp_df1,temp_df2,temp_df3])
#check if losses is in next
name_file = 'dla_piper.md'
# adjusted_ebitda_losses = '\n`\n\n\n'.join([x.replace('\n','') for x in test3.split('\n\n') if 'LOSSES' in x])
with open(f'./markdown/{name_file}', 'r', encoding="utf-8") as file:
    text = file.read()
    text = text.replace("**","")
sections = extract_headers_and_content(text, main_section_extract=False)
# Adjusted Ebitda:
financial_definitions = [x for x in sections if 'DEFINITIONS' in x[0].upper()]
adjusted_ebitda_exist = [x for x in financial_definitions if "ADJUSTED EBITDA" in x[1].upper()]

text = """(v) the aggregate amount of pro forma adjustments which may be taken into
account in any Relevant Period pursuant to paragraphs (c), (d) and (e) above,
when aggregated with Permitted Synergies taken into account in that
Relevant Period pursuant to paragraph (b) above, shall not exceed 20 per
cent of EBITDA for that Relevant Period;"""
