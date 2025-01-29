import pymupdf4llm
name_file = 'dla_piper'.replace(' ',"_")
md_text = pymupdf4llm.to_markdown("The-Facilities-Agreement.pdf")
# Save the Markdown to a file
with open(f'./markdown/{name_file}.md', 'w', encoding="utf-8") as file:
    file.write(md_text)