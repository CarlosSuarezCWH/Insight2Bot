from fastapi import FastAPI
from .routers import auth, pdfs, queries

app = FastAPI()
app.include_router(auth.router)
app.include_router(pdfs.router)
app.include_router(queries.router)

@app.get("/")
def read_root():
    return {"message": "RAG System"}
