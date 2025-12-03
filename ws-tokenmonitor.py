# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
# import openai
import ollama
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse
# # Set your OpenAI API Key
# openai.api_key = "your-api-key"
# FastAPI app
app = FastAPI()

# Prometheus metrics
token_counter_total = Counter("llm_tokens_total", "Total tokens used", ["model"])
token_counter_prompt = Counter("llm_tokens_prompt", "Prompt tokens used", ["model"])
token_counter_completion = Counter("llm_tokens_completion", "Completion tokens used", ["model"])

class PromptRequest(BaseModel):
    prompt: str
    model: str = "ipe"

@app.post("/chat")
async def chat(request: PromptRequest):
    # response = openai.ChatCompletion.create(
    #     model=request.model,
    #     messages=[{"role": "user", "content": request.prompt}],
    # )
    # usage = response['usage']
    # message = response['choices'][0]['message']['content']
    response = ollama.chat(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}]
    )
    # Ollama usage fields
    usage = {
        "prompt_tokens": response.get("prompt_eval_count", 0),
        "completion_tokens": response.get("eval_count", 0),
        "total_tokens": response.get("prompt_eval_count", 0) + response.get("eval_count", 0)
    }
    # Ollama response message
    message = response["message"]["content"]
    
    token_counter_prompt.labels(model=request.model).inc(usage["prompt_tokens"])
    token_counter_completion.labels(model=request.model).inc(usage["completion_tokens"])
    token_counter_total.labels(model=request.model).inc(usage["total_tokens"])
    return {
        "response": message,
        "usage": usage
    }
@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()