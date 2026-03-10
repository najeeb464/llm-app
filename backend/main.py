from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import init_db, insert_trace, get_traces, get_analytics
from classifier import classify_trace
from chatbot import generate_response, ChatRequest, ChatResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Support Chatbot & Observability API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TraceIn(BaseModel):
    user_message: str
    bot_response: str
    response_time: float


class TraceOut(BaseModel):
    id: int
    user_message: str
    bot_response: str
    category: str
    response_time: float
    timestamp: str



@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Generate a support response and save the trace."""
    bot_response, response_time = await generate_response(req.message)

    category = await classify_trace(req.message, bot_response)
    insert_trace(
        user_message=req.message,
        bot_response=bot_response,
        category=category,
        response_time=response_time,
    )

    return ChatResponse(response=bot_response, response_time=response_time)


@app.post("/traces", response_model=TraceOut)
async def create_trace(trace: TraceIn):
    """Receive a trace, classify it via LLM, save it, and return with classification."""
    category = await classify_trace(trace.user_message, trace.bot_response)
    saved = insert_trace(
        user_message=trace.user_message,
        bot_response=trace.bot_response,
        category=category,
        response_time=trace.response_time,
    )
    return TraceOut(**saved)


@app.get("/traces")
async def list_traces(category: Optional[str] = Query(None)):
    """Return all traces, most recent first. Optional category filter."""
    return get_traces(category=category)


@app.get("/analytics")
async def analytics():
    """Return aggregate stats: total, category breakdown, average response time."""
    return get_analytics()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse("static/dashboard.html")


@app.get("/dashboard")
async def serve_dashboard():
    return FileResponse("static/dashboard.html")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
