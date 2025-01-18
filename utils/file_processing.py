import PyPDF2
import docx

# Function ta3 extract text men el files
def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        # Ken el file type PDF
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        # Ken el file type DOCX
        return extract_text_from_docx(file_path)
    else:
        # Ken el format mch m3rouf
        raise ValueError("Unsupported file format")

# Function ta3 extract text men el PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            # Njib el text mel page
            text += page.extract_text()
    return text

# Function ta3 extract text men el DOCX
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    # Njib el text mel paragraphs
    return "\n".join([para.text for para in doc.paragraphs])
