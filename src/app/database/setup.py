from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from app.utils.text_processing import clean_text
from app.core.config import DATA_PATH, CHROMA_PATH, COHERE_API_KEY
import os
import shutil

# Configuración de la API KEY de Cohere
os.environ["COHERE_API_KEY"] = COHERE_API_KEY


def main():
    """
    Función principal para generar y almacenar la base de datos vectorial.
    Llama a las funciones para cargar documentos, dividir el texto y guardar en Chroma.
    """
    generate_data_store()


def generate_data_store():
    """
    Genera la base de datos vectorial cargando documentos, dividiéndolos en chunks
    y guardándolos en Chroma.
    """
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    """
    Carga todos los documentos con formato .docx desde un directorio especificado.

    Retorna:
        list[Document]: Una lista de objetos Document, donde cada objeto representa
        un documento .docx.
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.docx")
    documents = loader.load()
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)  # Limpiar el contenido del documento
    return documents


def split_text(documents: list[Document]):
    """
    Divide los documentos en chunks de texto más pequeños.

    Argumentos:
        documents (list[Document]): Una lista de documentos a dividir.

    Retorna:
        list[Document]: Una lista de documentos divididos en chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=470,  # Número de caracteres en cada chunk
        chunk_overlap=0,  # Número de caracteres que cada chunk se solapa con el siguiente
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Se dividieron {len(documents)} documentos en {len(chunks)} chunks")
    return chunks


def save_to_chroma(chunks: list[Document]):
    """
    Guarda los chunks de texto en la base de datos Chroma.

    Argumentos:
        chunks (list[Document]): Una lista de documentos divididos en chunks.
    """
    # Limpiar primero la base de datos
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Crear una base de datos nueva desde los documentos
    db = Chroma.from_documents(
        chunks,
        CohereEmbeddings(model="embed-multilingual-v3.0"),
        persist_directory=CHROMA_PATH
    )
    print(f"Se guardaron {len(chunks)} chunks en {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
