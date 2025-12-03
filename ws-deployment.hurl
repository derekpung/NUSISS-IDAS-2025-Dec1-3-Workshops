# Test docker model deployment endpoint
POST http://localhost:12434/v1/completions
Content-Type: application/json
{
  "model": "ai/smollm2:360M-Q4_K_M",
  "prompt": "Hello, who are you?",
  "max_tokens": 100
}
HTTP/1.1 200
