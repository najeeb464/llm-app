from google import genai
import os

import requests
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

VALID_CATEGORIES = [
    "Billing",
    "Refund",
    "Account Access",
    "Cancellation",
    "General Inquiry",
]

CLASSIFICATION_PROMPT = """You are a precise classification engine for a SaaS billing platform's customer support system. Your task is to classify a customer support conversation into exactly ONE category.

## Categories (with definitions)

1. **Billing** — Questions or issues about charges, invoices, payment methods, pricing plans, upgrades, downgrades, or billing cycles. Includes disputes about amounts charged.
2. **Refund** — Explicit requests to get money back, refund status inquiries, or discussions about refund eligibility and timelines.
3. **Account Access** — Problems logging in, password resets, two-factor authentication issues, locked accounts, email verification, or account recovery.
4. **Cancellation** — Requests to cancel a subscription, close an account, or stop a service. Includes questions about cancellation policies or what happens after cancelling.
5. **General Inquiry** — Anything that does not clearly fit the above four categories, including feature questions, general how-to questions, feedback, or greetings.

## Priority Rules for Ambiguous Messages

When a message touches multiple categories, apply this priority order:
- If cancellation is mentioned alongside billing concerns → **Cancellation** (the intent to cancel takes priority)
- If a refund is requested due to a billing error → **Refund** (the desired outcome takes priority)
- If account access issues are mentioned in context of billing → **Account Access** (the blocking issue takes priority)
- If the intent is still unclear after applying the above → **General Inquiry**

## Few-Shot Examples

User: "I was charged twice this month for my subscription"
Bot: "I apologize for the double charge. Let me look into your billing records."
Category: Billing

User: "I want my money back for last month, the service was down"
Bot: "I understand your frustration. Let me process a refund for you."
Category: Refund

User: "I can't log into my account and I need to check my invoice"
Bot: "Let me help you regain access to your account first."
Category: Account Access

User: "I want to cancel my subscription, and also I was overcharged last month"
Bot: "I'll help you with the cancellation and look into the overcharge."
Category: Cancellation

User: "What features are included in the Pro plan?"
Bot: "The Pro plan includes unlimited users, priority support, and advanced analytics."
Category: General Inquiry

## Instructions

Classify the following conversation. Respond with ONLY the category name — no explanation, no punctuation, no extra text. Your response must be exactly one of: Billing, Refund, Account Access, Cancellation, General Inquiry"""


# async def classify_trace(user_message: str, bot_response: str) -> str:
#     conversation_text = f'User: "{user_message}"\nBot: "{bot_response}"'

#     result = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=[
#             # {"role": "system", "text": CLASSIFICATION_PROMPT},
#             # {"role": "user", "text": conversation_text},
#              CLASSIFICATION_PROMPT,
#             conversation_text,
#         ],
#         config={
#             "temperature": 0,
#             "max_output_tokens": 10,
#         }
#     )

#     category = result.text.strip()
#     if category not in VALID_CATEGORIES:
#         category = "General Inquiry"

#     return category


def classify_trace(user_message: str, bot_response: str) -> str:
    conversation_text = f'User: "{user_message}"\nBot: "{bot_response}"'

    prompt = f"""
    {CLASSIFICATION_PROMPT}

    {conversation_text}

    Return ONLY the category name.
    """
    response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2", 
                "prompt": prompt,
                "stream": False
            }
        ).json()

    category = response["response"].strip()

    if category not in VALID_CATEGORIES:
        category = "General Inquiry"

    return category