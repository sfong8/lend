import pymupdf
# Open the PDF file
doc = pymupdf.open("output.pdf")
text = "\n".join([page.get_text() for page in doc])