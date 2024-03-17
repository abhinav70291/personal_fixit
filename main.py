
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from parse import parse_pdf
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Any, Dict, Optional
from typing import List
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from chunks_and_vectors import text_to_vector
from chunks_and_vectors import query_vectors
from document_list  import document_list, upload_pdf_name
from fastapi.responses import StreamingResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str
    file_name: str


@app.post("/parse_pdf_create_vector_database/")
async def parse_pdf_route(file: UploadFile):
    try:
        text = await parse_pdf(file)
        file_name = file.filename
        print("file_name:",file_name)
        await text_to_vector(text, file_name)
        return "chunks uploaded sucessfully on pinecone"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/")
async def chunk_and_vectorize_pdf(request: ChatRequest):
    text = request.text
    file_name = request.file_name

    if file_name=="ALL":
        file_name = None
    else:
        file_name = file_name
    response,chunks = await query_vectors(text,file_name)
    return {"response": response, "chunks": chunks}

@app.get("/document_list/")
def get_document_list():
    document_names = document_list()
    return document_names



