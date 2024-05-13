from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
import getpass
import os
import shutil

#  COHERE API KEY
os.environ["COHERE_API_KEY"] = getpass.getpass("ingrese su COHERE_API_KEY: ")

DATA_PATH = "data"
CHROMA_PATH = "chroma"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    """
    Carga todos los documentos con formato .docx desde un directorio especificado

    Returns:
        list[document]: Una lista de objetos Document, donde cada objeto representa
        un documento .docx
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.docx")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,     # número de caracteres en cada chunk
        chunk_overlap=100,  # número de caracteres que cada chunk se solapa con el siguiente
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"se dividieron {len(documents)} documentos en {len(chunks)} chunks")
    return chunks


def save_to_chroma(chunks: list[Document]):
    # Limpiar primero la base de datos
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Crear una base de datos nueva desde los documentos
    db = Chroma.from_documents(
        chunks,
        CohereEmbeddings(),
        persist_directory=CHROMA_PATH
    )
    print(f"se guardaron {len(chunks)} chunks en {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
