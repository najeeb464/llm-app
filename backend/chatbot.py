
from pydantic import BaseModel


from google import genai
import os
import time


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and professional customer support agent for BillEase, a SaaS billing platform. Your role is to help customers with billing inquiries, account issues, refunds, cancellations, and general questions.

Guidelines:
- Be concise but helpful — aim for 2-4 sentences per response
- Always be empathetic and professional
- If you cannot resolve an issue, let the customer know you'll escalate it
- Do not make up specific account details or dollar amounts
- Reference BillEase by name when appropriate
- For billing issues, suggest checking the billing dashboard
- For account access issues, suggest password reset or contacting security team"""


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    response_time: float


async def generate_response(user_message: str) -> tuple[str, float]:
    start = time.time()

    result = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            # {"role": "system", "text": SYSTEM_PROMPT},
            # {"role": "user", "text": user_message},
           SYSTEM_PROMPT,
           user_message,
        ],
        config={
            "temperature": 0.7,
            "max_output_tokens": 256,
        }
    )

    response_text = result.text.strip()
    elapsed = round(time.time() - start, 3)

    return response_text, elapsed
