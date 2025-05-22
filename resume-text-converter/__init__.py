import azure.functions as func
import io
import PyPDF2
from docx import Document
 
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get file from request
    file = req.files.get('file')
    if not file:
        return func.HttpResponse("No file received", status_code=400)
    # Convert based on file type
    try:
        if file.filename.endswith('.pdf'):
            text = extract_pdf_text(file.stream)
        elif file.filename.endswith('.docx'):
            text = extract_docx_text(file.stream)
        else:
            return func.HttpResponse("Unsupported file type", status_code=400)
        return func.HttpResponse(text, mimetype="text/plain")
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
 
def extract_pdf_text(stream):
    reader = PyPDF2.PdfReader(stream)
    return "\n".join([page.extract_text() for page in reader.pages])
 
def extract_docx_text(stream):
    doc = Document(io.BytesIO(stream.read()))
    return "\n".join([para.text for para in doc.paragraphs])