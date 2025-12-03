# Test /chat endpoint
POST http://localhost:8000/chat
Content-Type: application/json
{
  "prompt": "Hello Ollama, how are you?"
}
HTTP/1.1 200
[Asserts]
jsonpath "$.response" exists
jsonpath "$.usage.prompt_tokens" exists
jsonpath "$.usage.completion_tokens" exists
jsonpath "$.usage.total_tokens" exists


# Test /metrics endpoint
GET http://localhost:8000/metrics
HTTP/1.1 200
[Asserts]
body contains "llm_tokens_total"
body contains "llm_tokens_prompt"
body contains "llm_tokens_completion"
