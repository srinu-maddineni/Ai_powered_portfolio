from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from Email_server import send_email
from rag_rag.embeding import query
from rag_rag.gemini import gemini

app = FastAPI(title="RAG Email API", version="1.0.0")

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Models ────────────────────────────────────────────────────────────

class VisitorEmailRequest(BaseModel):
    """Only the visitor's email is needed — subject and body are fixed."""
    recipient_email: EmailStr


class QueryRequest(BaseModel):
    """User's natural language question for the RAG pipeline."""
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query text must not be empty or whitespace.")
        return v.strip()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "RAG API is running"}


@app.post("/send-thankyou-email", summary="Send a 'Thanks for visiting' email to the user")
def send_thankyou_email(payload: VisitorEmailRequest):
    result = send_email(recipient_email=payload.recipient_email)

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))

    return result


@app.post("/query", summary="Ask a question about Srinu Maddineni's portfolio")
def query_endpoint(payload: QueryRequest):
    try:
        result = query(payload.text)
        answer = gemini(payload.text, result)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")