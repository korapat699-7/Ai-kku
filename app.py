import os
from flask import Flask, request, Response, jsonify
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# ตั้งค่าตาม Resource ของคุณ
ENDPOINT = "https://ai-korapatseedamarts3335ai740227246567.services.ai.azure.com/models"
MODEL_NAME = "DeepSeek-R1"
API_KEY = "AkKXLqebVy8r1ZoYitLx3KjPxHRiWSL7FGSyN1g6pRamAsQUS2XtJQQJ99BBACHYHv6XJ3w3AAAAACOG2XtG"

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY),
)

@app.route("/")
def index():
    # เสิร์ฟหน้าเว็บหลัก (index.html)
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    ตัวอย่าง JSON ที่ Frontend ส่งมา:
    {
      "messages": [
         {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": "Hello"},
         {"role": "assistant", "content": "Hi there! How can I help?"},
         {"role": "user", "content": "Tell me a joke"}
      ]
    }
    """
    data = request.json
    messages = data.get("messages", [])

    # เรียก ChatCompletions แบบ Streaming
    try:
        completion = client.complete(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=4096,
            temperature=0.5,
            stream=True  # <<--- โหมดสตรีม
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # สร้าง generator เพื่อส่ง token ทีละ chunk กลับไป
    def stream_response():
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta:
                text = chunk.choices[0].delta.content
                if text:
                    yield text

    # ส่ง response เป็น text/plain แบบ streamed
    return Response(stream_response(), mimetype="text/plain")

if __name__ == "__main__":
    # รัน Flask
    app.run(debug=True, port=5000)
