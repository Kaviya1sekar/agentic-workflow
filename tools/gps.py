from langchain.tools import tool
import fitz
import os

class PDFReaderTool:
    @staticmethod
    @tool("Pdf Reader")
    def read_pdf(path: str) -> str:
        """
        This tool reads the content of a file.
        The input should be a string representing the path to the file.
        """
        try:
            with open(path, 'rb') as file:
                content = file.read()
            content_type = path.split(".")[-1]

            if content_type == 'pdf':
                text = []
                with fitz.open(stream=content, filetype="pdf") as doc:
                    for page in doc:
                        text.append(page.get_text())
                return '\n'.join(text)  # Return concatenated text from all pages
            else:
                return content.decode('utf-8', errors='ignore')  # Return raw content if not a PDF

        except FileNotFoundError:
            return f"Error: File '{path}' not found."
        except Exception as e:
            return f"An error occurred: {e}"