import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from rag_utils import query_email_assistant
import traceback

app = FastAPI()

app.mount("/static", StaticFiles(directory="api/static"), name="static")
templates = Jinja2Templates(directory="api/templates")

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query_email")
async def query_email(request: QueryRequest):
    try:
        if not request.query.strip():
            return JSONResponse(status_code=400, content={"error": "Query cannot be empty."})

        response = query_email_assistant(request.query)
        return {"response": response}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "An error occurred while processing the query."})
