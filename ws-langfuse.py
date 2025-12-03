from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langfuse import Langfuse
from openai import OpenAI
# Load environment variables from .env or .env.template
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists(".env.template"):
    load_dotenv(".env.template")
# Initialize Langfuse client
lf = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
)
# Initialize OpenAI
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=openai_api_key
)
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "message is required"}), 400
    try:
        # Create a trace for this request
        trace = lf.trace(
            name="chat-endpoint",
            user_id=data.get("user_id", "anonymous")
        )
        # Create a span for the OpenAI call
        span = trace.span(name="openai-completion")
        # Make the OpenAI API call
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": data["message"]}]
        )
        answer = resp.choices[0].message.content
        # End the span with the result
        span.end(
            output=answer,
            metadata={
                "model": "gpt-4",
                "completion_tokens": len(answer)
            }
        )
        # Score the response
        trace.score(
            name="response_length",
            value=len(answer)
        )
        lf.flush()
        return jsonify({
            "response": answer,
            "trace_id": trace.id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=4000, debug=debug_mode)