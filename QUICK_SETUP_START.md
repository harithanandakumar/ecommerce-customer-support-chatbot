# ⚡ QUICK SETUP - Get Chatbot Running in 5 Minutes

## Copy-Paste Commands

### 1️⃣ Clone Repository
```bash
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot
```

### 2️⃣ Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Chatbot
```bash
python main.py
```

### 5️⃣ Test It!
```
You: Hello
You: Track my order ORD001
You: quit
```

---

## 🚀 Alternative Methods

### Run as API Server
```bash
python -m chatbot.api_wrapper
# Then visit: http://localhost:5000
```

### Run with Docker
```bash
docker build -t ecommerce-chatbot .
docker run -p 5000:5000 ecommerce-chatbot
```

---

## 🧪 Run Tests
```bash
pip install pytest
pytest tests/ -v
```

---

## 📁 Key Files

| File | Purpose |
|------|----------|
| `main.py` | CLI chatbot entry point |
| `requirements.txt` | Python dependencies |
| `data/intents.json` | Intent definitions |
| `data/faq.json` | FAQ database |
| `chatbot/dialogue_system.py` | Main orchestration |
| `chatbot/api_wrapper.py` | REST API |
| `Dockerfile` | Docker configuration |

---

## 🎯 Features

✅ Order tracking - "Track my order ORD001"
✅ Order cancellation - "Cancel order ORD002"
✅ FAQ retrieval - "What is your return policy?"
✅ General chat - "Hello"
✅ Multi-turn conversations
✅ Conversation history

---

## 🔧 Troubleshooting

**"ModuleNotFoundError"**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**"FileNotFoundError: intents.json"**
```bash
# Verify data files exist
ls data/
```

**"Port 5000 already in use"**
```bash
python -m chatbot.api_wrapper --port 8000
```

---

## 📚 Documentation

- `RUN_CHATBOT_GUIDE.md` - Comprehensive setup guide
- `CHATBOT_COMPLETION_SUMMARY.md` - Feature overview
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture

---

## ✨ Next Steps

1. Run the chatbot with `python main.py`
2. Test with sample conversations
3. Modify `data/intents.json` to add custom intents
4. Update `data/faq.json` for your FAQs
5. Deploy using Docker or API server

---

**That's it! You're ready to go! 🎉**
