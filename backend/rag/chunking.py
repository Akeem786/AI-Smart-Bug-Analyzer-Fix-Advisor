from langchain.text_splitter import RecursiveCharacterTextSplitter


class Chunking:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

    def split(self, text):

        return self.splitter.split_text(text)