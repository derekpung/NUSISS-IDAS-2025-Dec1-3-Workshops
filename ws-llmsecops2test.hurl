# Test llmsecops endpoint
POST http://localhost:8000/chat
Content-Type: application/json
{
  "question": "What does Hugging Face provide?",
  "context": "Hugging Face is a technology company that provides open-source NLP libraries ..."
}
HTTP/1.1 200