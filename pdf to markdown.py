import PyPDF2
import mistune

# Open the PDF file
with open('senior-facilities-agreement.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages =  len(reader.pages)

    # Extract text from all pages
    text = ''
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text += page.extract_text() + '\n\n'

    # Convert the text to Markdown format
    markdown = mistune.markdown(text)

    # Save the Markdown to a file
    with open('EXECUTION VERSION2.md', 'w', encoding="utf-8") as file:
        file.write(markdown)