# Test langfuse
POST http://localhost:4000/chat
Content-Type: application/json
{
  "message": "What is the capital of France?",
  "user_id": "test-user"
}
HTTP/1.1 200