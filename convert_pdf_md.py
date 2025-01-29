import pymupdf4llm
name_file = 'COBHAM ULTRA'.replace(' ',"_")
md_text = pymupdf4llm.to_markdown("senior-facilities-agreement.pdf")

# Save the Markdown to a file
with open(f'./markdown/{name_file}.md', 'w', encoding="utf-8") as file:
    file.write(md_text)