from fastapi import FastAPI
from app.api import endpoints

app = FastAPI()

# Incluir las rutas del enrutador
app.include_router(endpoints.router)

# Punto de entrada para ejecutar la aplicación FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
