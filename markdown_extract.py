import re

# Read the markdown file as text
with open('EXECUTION VERSION2.md', 'r', encoding="utf-8") as file:
    markdown_content = file.read()
## table of contents
# Extract the table of contents using regex
toc_pattern = re.compile(r'<ol>(.*?)</ol>', re.DOTALL)
toc_match = toc_pattern.search(markdown_content)

if toc_match:
    toc_html = toc_match.group(1)
    toc_items = re.findall(r'<li>(.*?)</li>', toc_html)

    # Print the table of contents
    for item in toc_items:
        print(item.strip())

toc_items2 = [x.split('...')[0].strip().lower() for x in toc_items]


# Regular expression to match numbered sections
# section_pattern = re.compile(r'(\d+\.\s+[A-Z\s]+)', re.MULTILINE)
section_pattern = re.compile(r'^(\d+\.\s+[A-Z\s–]+)', re.MULTILINE)
text=markdown_content
# Find all matches
sections = section_pattern.findall(text)
# Convert toc_items2 to a set of lowercase items for efficient lookup
toc_items2_set = {item.lower() for item in toc_items2}

# Filter sections to include only those that contain a substring from toc_items2
filtered_sections = [
    section for section in sections
    if any(toc_item.lower() in section.lower() for toc_item in toc_items2)
]

# Extract text between sections
section_texts = {}
last_section = None
last_index = 0

for match in section_pattern.finditer(text):
    section = match.group(1)
    start_index = match.start()
    if last_section:
        section_texts[last_section] = text[last_index:start_index].strip()
    last_section = section
    last_index = start_index

# Add the text after the last section
if last_section:
    section_texts[last_section] = text[last_index:].strip()

# Print the extracted sections and their corresponding text
for section, text in section_texts.items():
    print(f"Section: {section}")
    print(f"Text: {text}\n")

# Output the final section separately if needed
if sections:
    print(f"Section: {sections[-1]}")
    print(f"Text: {section_texts[sections[-1]]}")


# equity cure example
financial_covant = list(section_texts.keys())
financial_covant2 = [x for x in financial_covant if 'EVENTS OF DEFAULT' in x  ]

event_default = section_texts[financial_covant2[0]]
equity_cure_pattern = re.compile(
    r"(b)\s*Equity Cure\s*(.*?)(?=(?:\n\n|\n\d+\.))",
    re.DOTALL
)

# Search for the equity cure section
equity_cure_match = equity_cure_pattern.search(event_default)

if equity_cure_match:
    equity_cure_text = equity_cure_match.group(2).strip()
    print("Equity Cure Key Terms:")
    print(equity_cure_text)
else:
    print("Equity Cure section not found.")