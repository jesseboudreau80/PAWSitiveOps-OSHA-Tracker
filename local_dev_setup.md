# 🧰 Local Development & n8n Integration Guide

This document outlines how to run the **PAWSitiveOps OSHA Tracker** locally, sync your environments between Codespaces and Warp, and expose your local n8n workflows to the web for testing.

---

## 🧭 1️⃣ Local Git Sync: Warp ↔ Codespaces

You can work seamlessly between your work Codespace and your home Warp setup.

### ✅ Daily Sync Routine

**Before starting work (in either environment):**
```bash
git pull origin main
After finishing work:

git add .
git commit -m "Describe what you changed"
git push origin main


When switching machines:

git pull origin main


If you ever get a merge warning:

git pull origin main --rebase

⚙️ 2️⃣ Running FastAPI Backend Locally
cd ~/PAWSitiveOps-OSHA-Tracker
source venv/bin/activate
uvicorn app.main:app --reload


The backend will run at:

http://127.0.0.1:8000

💻 3️⃣ Running Next.js Frontend Locally
cd ~/PAWSitiveOps-OSHA-Tracker/frontend
npm install
npm run dev


Then open:

http://localhost:3000

🔄 4️⃣ Running n8n Locally (Automation Engine)

n8n is your workflow automation layer (for generating OSHA reports, handling alerts, and syncing safety data).

▶️ Option A: Run locally with tunnel (quick setup)
npx n8n start --tunnel


This creates a public URL like:

https://unique-subdomain.n8n.cloud/webhook/test


Now your local webhooks are accessible from anywhere.

▶️ Option B: Use ngrok for a stable tunnel
sudo snap install ngrok
n8n start
ngrok http 5678


ngrok will display:

Forwarding  https://yourname.ngrok.io -> http://localhost:5678

🔒 Secure your n8n instance

Add basic authentication before exposing your instance:

export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=jesse
export N8N_BASIC_AUTH_PASSWORD=supersecret
n8n start --tunnel


Or save these in an .env file in your n8n directory.

🧩 5️⃣ FastAPI → n8n Integration Example

In your FastAPI app, you can trigger n8n workflows like this:

import requests

requests.post("https://your-tunnel-url/webhook/osha-report", json={
    "center_id": 113,
    "incident_type": "bite",
    "injury_severity": "minor"
})

💡 6️⃣ Summary
Task	Command
Pull latest repo	git pull origin main
Push new changes	git push origin main
Run backend	uvicorn app.main:app --reload
Run frontend	npm run dev
Run n8n local tunnel	npx n8n start --tunnel
Secure n8n	export N8N_BASIC_AUTH_ACTIVE=true
Test API to n8n	requests.post("<your-n8n-url>", json=data)

Pro Tip:
Create a helper script for quick syncing:

echo '#!/bin/bash
git fetch origin main
git pull origin main --rebase
git push origin main
' > sync.sh
chmod +x sync.sh


Run ./sync.sh anytime to update both your local and remote branches.


---

### 📦 To add this file from Warp:

```bash
cd ~/PAWSitiveOps-OSHA-Tracker
nano LOCAL_DEV_SETUP.md


Paste everything above → save → exit (Ctrl+O, Enter, Ctrl+X).

Then commit it:

git add LOCAL_DEV_SETUP.md
git commit -m "Add local development and n8n setup guide"
git push origin main
