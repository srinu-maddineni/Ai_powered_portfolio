from google import genai
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\srinu\OneDrive\Desktop\rag\backend\app\.env")

client = genai.Client(api_key=os.getenv("GEMINI_AI_API"))

# Always injected — guarantees identity facts reach the LLM even if the
# retrieval step misses the intro chunk.
_IDENTITY = """
PORTFOLIO OWNER IDENTITY (always true, use this for any identity question):
- Full Name: Srinu Maddineni
- Role: Software Engineer / Full-Stack (MERN) Developer
- Email: maddinenis76@gmail.com | Phone: 8374428832
- Portfolio: https://srinu-maddineni.github.io/Portfolio/
- GitHub: https://github.com/srinu-maddineni
- LinkedIn: https://www.linkedin.com/in/srinu-maddineni-aa6835290/
- College: Lendi Institute of Engineering and Technology, B.Tech ECE, CGPA 7.2, May 2026
- Internship: Software Engineer Intern at Tilicho Labs (Jan 2026 – May 2026)
- LeetCode: 549 problems solved, Rating 1491
""".strip()


def gemini(question: str, result: dict) -> str:
    # ChromaDB returns {'documents': [[chunk1, chunk2, ...]], ...}
    chunks = result.get("documents", [[]])[0]
    retrieved_context = "\n\n---\n\n".join(chunks)

    message = f"""You are an intelligent AI assistant for Srinu Maddineni's portfolio website.
Your job is to answer any question a recruiter, visitor, or curious person might ask about Srinu.

RULES:
- Answer using the IDENTITY block and RETRIEVED CONTEXT below.
- Be specific, accurate, and helpful.
- If a question is about who owns this portfolio or what the name of this portfolio is, always answer: "Srinu Maddineni".
- For factual questions (skills, projects, contact, education, experience), give direct and complete answers.
- For subjective questions (strengths, why hire him, etc.), answer positively based on the context.
- If the context truly doesn't have the answer, say so honestly.
- Do NOT make up information not present in the context.

{_IDENTITY}

RETRIEVED CONTEXT:
{retrieved_context}

QUESTION:
{question}

ANSWER:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message
    )
    return response.text
