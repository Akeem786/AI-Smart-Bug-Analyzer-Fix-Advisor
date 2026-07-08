from pypdf import PdfReader
import os

class FileParser:

    @staticmethod
    def parse(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".txt":

            with open(file_path,"r",encoding="utf-8") as f:

                return f.read()

        elif extension == ".log":

            with open(file_path,"r",encoding="utf-8") as f:

                return f.read()

        elif extension == ".pdf":

            reader = PdfReader(file_path)

            text = ""

            for page in reader.pages:

                text += page.extract_text()

            return text

        return ""