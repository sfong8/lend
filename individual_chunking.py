import re

with open('EXECUTION VERSION2.md', 'r', encoding="utf-8") as file:
    markdown_content = file.read()
# Define a regular expression to find headings and subheadings
heading_pattern = re.compile(r'(\d+\.\d*\s+[A-Z].*)')

# Split the text into sections based on the headings
sections = heading_pattern.split(markdown_content)

# Filter out empty strings and combine headings with their corresponding text
chunks = []
current_chunk = ""
for section in sections:
    if heading_pattern.match(section):
        if current_chunk:
            chunks.append(current_chunk.strip())
        current_chunk = section
    else:
        current_chunk += " " + section
if current_chunk:
    chunks.append(current_chunk.strip())

# Print the chunks
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)
    print("\n" + "-"*40 + "\n")

financial_convenent = [x for x in chunks if 'EQUITY CURE' in x.upper()]