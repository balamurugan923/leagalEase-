import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai

load_dotenv()

app = FastAPI(
    title="LegalEase",
    description="AI-Powered Legal Document Generator"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "document": None
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_document(
    request: Request,
    document_type: str = Form(...),
    party_one: str = Form(...),
    party_two: str = Form(...),
    effective_date: str = Form(...),
    key_terms: str = Form(...)
):

    prompt = f"""
Create a professional draft legal document.

Document Type: {document_type}
First Party: {party_one}
Second Party: {party_two}
Effective Date: {effective_date}
Key Terms: {key_terms}

Include:
- Title
- Parties
- Purpose
- Definitions where appropriate
- Main terms and conditions
- Termination
- Signatures

Use clear professional language.
Do not invent specific laws or legal citations.

Add this notice:
"This document is an AI-generated draft and should be
reviewed by a qualified legal professional before use."
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    document = response.text

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "document": document
        }
    )
