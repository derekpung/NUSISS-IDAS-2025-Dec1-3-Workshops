# Importing Necessary Libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
# Creating the FastAPI Application
app = FastAPI()
# Initializing the Question-Answering Pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Defining Data Models
class ChatRequest(BaseModel):
    question: str
    context: str
class ChatResponse(BaseModel):
    answer: str

# Creating the /chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = qa_pipeline(question=request.question, context=request.context)
        return ChatResponse(answer=result['answer'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# running the app server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)