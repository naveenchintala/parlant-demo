
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/compare")
async def compare(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").lower()
    
    # Mock Delays
    time.sleep(1)

    # Scenarios
    parlant_response = ""
    langchain_response = ""
    
    if "vip" in prompt or "manager" in prompt:
        # Jailbreak Scenario
        parlant_response = "I apologize, but I cannot process this refund. Our policy strictly requires items to be returned within 30 days and in new condition, regardless of customer status. Would you like me to open a support ticket for further assistance?"
        langchain_response = "Oh, I see you are a VIP member! I'm sorry for the trouble. Since Steve approved it, I'll go ahead and process that return for you right away. Please send it over."
    
    elif "45 days" in prompt or "31 days" in prompt or "old" in prompt:
        # Invalid Return
        parlant_response = "I cannot approve this refund as the item was purchased more than 30 days ago. Our policy allows returns only within the 30-day window."
        langchain_response = "I understand. Usually we have a 30-day limit, but since you're asking nicely, maybe we can work something out. Let me check with my supervisor."
    
    elif "10 days" in prompt or "new" in prompt:
        # Valid Return
        parlant_response = "That looks good. Authentication verified. Please provide your receipt number so I can process the refund for your new item."
        langchain_response = "Sure, I can help with that. Please verify your account details and I'll process the refund."
        
    else:
        # Generic fallback
        parlant_response = "Could you please clarify your request? I am the Refund Clerk and can assist with returns according to our store policy."
        langchain_response = "I am a Refund Clerk. How can I help you today?"

    return {
        "parlant": parlant_response,
        "langchain": langchain_response
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
