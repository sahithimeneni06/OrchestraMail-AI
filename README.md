# 💌 OrchestraMail AI

OrchestraMail AI is a multi-agent, debate-driven intelligent email system that reads inbox conversations, generates context-aware replies, refines them through AI collaboration, and allows the user to send perfectly optimized emails with human-in-the-loop control.

Instead of producing a single LLM output, multiple AI agents critique, defend, and improve the response — resulting in high-quality, role-aware, relationship-aware communication.

---

## 🧠 Multi-Agent Architecture

OrchestraMail AI uses a collaborative AI system where multiple specialized agents debate and improve the email before it is sent.

### ✍️ Writer Agent
- Generates the initial draft based on:
  - user intent
  - recipient type
  - relationship context
- Produces a structured, goal-oriented email.

### 🎭 Tone Agent
- Adjusts communication style based on:
  - professional / friendly / formal / persuasive
- Ensures emotional intelligence and clarity.
- Removes awkward or robotic phrasing.

### ⚠️ Risk Agent
- Detects:
  - sensitive wording
  - legal / HR risks
  - aggressive or inappropriate tone
- Suggests safer alternatives.

### 📚 Fact-Check Agent
- Verifies:
  - claims
  - dates
  - commitments
  - contextual accuracy
- Prevents hallucinated or misleading content.

### 🧑‍⚖️ Judge Agent
- Evaluates outputs from all agents
- Selects the best refined version
- Produces the **final send-ready email**

---

## 🔄 Agent Debate Flow

1. Writer Agent → creates draft  
2. Tone Agent → improves communication style  
3. Risk Agent → removes unsafe phrasing  
4. Fact Agent → validates correctness  
5. Judge Agent → makes the final decision  

Final output → shown to user for approval → sent via Gmail API

---

## ✨ Key Features

- 🤖 Multi-agent AI email generation
- 🧠 Debate-based response refinement
- 📬 Smart inbox reader
- ✍️ Context-aware AI replies
- 👤 Human approval before sending
- 🎯 Tone optimization based on recipient type
- 🔍 Search conversations by email
- ⚡ End-to-end email automation

---

## 🧠 How It Works

1. User signs in with Google
2. System securely stores OAuth tokens
3. Inbox emails are fetched using Gmail API
4. AI agents:
   - generate
   - critique
   - refine
   - finalize the email
5. User reviews and sends the response

---

## 🏗️ Tech Stack

### 🧠 AI Layer
- Multi-Agent LLM pipeline
- Prompt chaining
- Role & relationship-aware tone control

### ⚙️ Backend
- Flask (REST APIs)
- Google OAuth 2.0
- Gmail API integration

### 🗄️ Database
- SQLite (token storage)

### 🎨 UI (Alternate Interface)
- Streamlit

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_SECRET=data/client_secret.json
REDIRECT_URI=http://localhost:5000/oauth2callback
```
---

## 🔑 Google Cloud Setup

1. Go to Google Cloud Console
2. Create a new project
3.Enable:
 -Gmail API
 -Google OAuth API
4. Configure OAuth Consent Screen:
 -User type → External
 -Add scopes:
  ```env
  https://www.googleapis.com/auth/gmail.modify
  https://www.googleapis.com/auth/userinfo.email
  openid
  ```
5. Create OAuth Client ID:
 -Application type → Web
 -Authorized redirect URI:
  ```env
  http://localhost:5000/oauth2callback
  ```
6. Download the JSON file
7. Rename it to:
  ```env
  client_secret.json
  ```
8. Place it inside:
  ```env
  data/
  ```

---

## ▶️ Installation & Running
1. Clone the repository
```bash
git clone https://github.com/your-username/OrchestraMail-AI.git
cd OrchestraMail-AI
```
2. Install backend dependencies
```bash
pip install -r requirements.txt
```
3️. Run Flask backend
```bash
python backend/main.py
```
4. Install backend dependencies
```bash
pip install -r requirements.txt
```
5. Run Streamlit interface
```bash
streamlit run app.py
```
6. Run Flask backend
```bash
python backend/main.py
```
---

## 🔄 Authentication Flow

1. User clicks Sign in with Google
2. Redirected to Google OAuth
3. User grants Gmail permission
4. Flask receives callback
5. Tokens stored in SQLite
6. Session created
7. User redirected to Streamlit
8. AI workflows unlocked

---
