import docx
import PyPDF2
from pathlib import Path


def readDocx(document):
    document = docx.Document(document)
    return ". ".join(para.text.lower() for para in document.paragraphs)


def readPDF(document):
    pdfFileObj = open(document, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    content = ". ".join([pdfReader.getPage(page).extractText().lower()
                         for page in range(pdfReader.numPages)])
    return content


def getText(document):
    p = Path(document)
    extension = p.suffix
    if extension == ".docx":
        return readDocx(document)
    else:
        return readPDF(document)
