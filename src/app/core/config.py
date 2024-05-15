import os


# Configuración de la API KEY de Cohere
COHERE_API_KEY = "sfJ8x2tthKmqJManrr3wDCseP5AAqZ8SRykUlens"
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

# Ruta de los datos y de la base de datos Chroma
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(BASE_DIR, "data")
CHROMA_PATH = os.path.join(BASE_DIR, "app", "database", "chroma")

