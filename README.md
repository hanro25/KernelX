# OpsPilot AI — MVP

A beginner-friendly web prototype for AI-assisted Linux and AWS troubleshooting. It analyses user-provided descriptions and text logs; it does **not** connect to servers or execute commands.

## Requirements

- Python 3.10 or newer
- An API key from your chosen AI provider (this starter uses the OpenAI API)
- Internet connection

## Run locally

### 1. Create and activate a virtual environment

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure your API key

Copy `.env.example` to `.env` and edit `.env`:

```env
OPENAI_API_KEY=your_real_api_key
OPENAI_MODEL=gpt-4o-mini
```

Keep `.env` private. Never commit it to Git or paste the key into chats, screenshots, or source code. API usage may incur charges; set a budget/usage limit with your provider before testing.

### 4. Start the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

## First test

Try a harmless test case such as:

> Linux server reports `No space left on device`. Please explain safe diagnostic commands. Do not assume you can access the server.

Then test with a short, redacted sample log.

## Important MVP limitations

- No server access, shell execution, AWS credentials, or automated remediation.
- No user accounts or persistent incident history.
- Uploaded logs are sent to the configured AI API for analysis. Remove sensitive information first and review the provider's data handling terms.
- AI output can be incorrect. Validate recommendations against your operational standards.
- This is a prototype, not an enterprise-ready or production incident-response system.

## Suggested next milestones

1. Add curated troubleshooting playbooks and test cases.
2. Add a local demo mode with fixed example answers.
3. Add authentication and usage limits before inviting external users.
4. Add structured output, citations to trusted documentation, and an evaluation suite.
5. Only later consider read-only integrations with explicit user approval and audit logging.
