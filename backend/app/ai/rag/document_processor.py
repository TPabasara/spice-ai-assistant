import fitz  # PyMuPDF
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """
    Handles extracting text from PDFs and splitting it into semantically meaningful chunks.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # We use overlap so if a concept spans two chunks, the context isn't lost
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extracts raw text from a PDF file."""
        text = ""
        try:
            # Open the PDF using PyMuPDF
            with fitz.open(file_path) as pdf_document:
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    text += page.get_text()
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def create_chunks(self, text: str) -> List[str]:
        """Splits raw text into smaller overlapping chunks."""
        if not text.strip():
            return []
        return self.text_splitter.split_text(text)