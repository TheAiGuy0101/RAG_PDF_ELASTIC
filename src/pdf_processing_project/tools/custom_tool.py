import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

class PDFProcessingTool:
    def __init__(self, tesseract_cmd):
        self.tesseract_cmd = tesseract_cmd
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

    def extract_text(self, file_path):
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                # Perform OCR
                images = convert_from_path(file_path, first_page=page_num + 1, last_page=page_num + 1)
                for image in images:
                    text += pytesseract.image_to_string(image)
        return text

# Usage example
if __name__ == "__main__":
    tool = PDFProcessingTool(tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    text = tool.extract_text('example.pdf')
    print(text)
