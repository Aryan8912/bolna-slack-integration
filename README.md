# Bolna → Slack Integration

A production-ready FastAPI integration that listens to webhook events from Bolna and sends formatted Slack alerts whenever a call ends.

---

# 🚀 Features

- ✅ FastAPI webhook server
- ✅ Receives Bolna webhook events
- ✅ Parses real Bolna payloads
- ✅ Sends Slack notifications automatically
- ✅ Environment variable support with `.env`
- ✅ Local testing with Swagger UI / curl
- ✅ Async HTTP requests using `httpx`
- ✅ Clean and minimal project structure

---

# 🏗️ Architecture

```text
Bolna Webhook -> FastAPI Endpoint -> Payload Parsing -> Slack Notification
```

---

# 📂 Project Structure

```text
bolna-slack-integration/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirement.txt
└── README.md
```

---

# ⚙️ Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- httpx
- python-dotenv
- Slack Incoming Webhooks

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone https://github.com/Aryan8912/bolna-slack-integration.git
cd bolna-slack-integration
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirement.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX
```

---

# 🔔 Slack Webhook Setup

1. Create a Slack App  
2. Enable Incoming Webhooks  
3. Add webhook to workspace  
4. Copy generated webhook URL  

Slack Docs:  
https://api.slack.com/messaging/webhooks

---

# ▶️ Run Locally

From project root:

```bash
uvicorn app.main:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

# 📡 Webhook Endpoint

## POST `/webhook/bolna`

Receives webhook events from Bolna.

---

# 🧪 Example Webhook Payload

```json
{
  "id": "call_test_001",
  "agent_id": "d311e737-70e6-4075-bef6-c0ef3a7026b4",
  "status": "completed",
  "transcript": "Hello, this is a real webhook payload test from Bolna.",
  "conversation_time": 128.5,
  "total_cost": 0.42,
  "telephony_data": {
    "duration": 128,
    "to_number": "+919999999999",
    "from_number": "+918888888888",
    "recording_url": "https://example.com/recording.mp3",
    "call_type": "outbound",
    "provider": "twilio",
    "hangup_by": "agent",
    "hangup_reason": "completed"
  }
}
```

---

# 🧪 Test Using curl

```bash
curl -X POST http://127.0.0.1:8000/webhook/bolna \
-H "Content-Type: application/json" \
-d @payload.json
```

---

# 📨 Example Slack Alert

```text
📞 Bolna Call Ended

Call ID: call_test_001
Agent ID: d311e737-70e6-4075-bef6-c0ef3a7026b4
Duration: 128.5 sec

Transcript:
Hello, this is a real webhook payload test from Bolna.
```

---

# 📋 Example Terminal Output

```text
Received Payload:
{
  'id': 'call_test_001',
  'agent_id': 'd311e737-70e6-4075-bef6-c0ef3a7026b4'
}

Webhook URL:
https://hooks.slack.com/services/...

Slack Status: 200
Slack Response: ok
```

---

# ✅ Requirements Fulfilled

- ✔ Receive webhook events from Bolna
- ✔ Detect completed calls
- ✔ Extract:
  - id
  - agent_id
  - duration
  - transcript
- ✔ Send formatted Slack alerts
- ✔ FastAPI webhook implementation
- ✔ Local testing support

---

# 🔮 Future Improvements

- Database storage (SQLite/PostgreSQL)
- Retry mechanism for failed Slack requests
- Structured logging
- Docker support
- Deployment on Render/Railway/AWS
- Authentication & webhook verification

---

# 📚 References

- Bolna API Docs  
  https://www.bolna.ai/docs

- Slack API Docs  
  https://docs.slack.dev

- FastAPI Docs  
  https://fastapi.tiangolo.com

---

# 👨‍💻 Author

Aryan Pandey

GitHub:  
https://github.com/Aryan8912
