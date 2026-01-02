# Quick Start Guide - Backend Setup

## 5-Minute Setup

### Step 1: Get Groq API Key (2 minutes)
1. Go to https://console.groq.com/keys
2. Sign up if needed and create a new API key
3. Copy the key

### Step 2: Configure Backend (2 minutes)
1. Open `backend/.env` file
2. Find `GROQ_API_KEY=your_groq_api_key_here`
3. Replace with your actual API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
4. Save the file

### Step 3: Install & Run (1 minute)

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

That's it! The API is now running on `http://localhost:5000`

---

## Testing the Backend

### 1. Check Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "healthy", "success": true}
```

### 2. Create a Test Account
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

You'll get back a token in the response.

### 3. Analyze a Policy
```bash
curl -X POST http://localhost:5000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "policyText": "We seek young and energetic candidates who are digital natives and able-bodied to handle our fast-paced environment.",
    "policyName": "Test Policy"
  }'
```

The API will analyze the text using Groq's LLM and return detected biases.

---

## Connecting Frontend to Backend

Update your frontend API calls to point to the backend:

```javascript
// In your frontend code
const API_URL = 'http://localhost:5000/api';

// Example analysis call
const response = await fetch(`${API_URL}/analysis/analyze`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    policyText: policyContent,
    policyName: policyName
  })
});
```

---

## Common Issues

### Port 5000 Already in Use
Change port in `.env`:
```
FLASK_PORT=8000
```

### API Key Error
Make sure `.env` has your actual Groq API key:
```bash
# Verify it's set
echo $GROQ_API_KEY  # Linux/macOS
echo %GROQ_API_KEY%  # Windows PowerShell
```

### Module Not Found
Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

---

## Useful Commands

### Restart Backend
```bash
# Press Ctrl+C to stop
# Then run again:
python main.py
```

### Reset Database
```bash
# Delete the database file (it will recreate on startup)
rm policy_bias.db     # Linux/macOS
del policy_bias.db    # Windows
```

### Check Logs
The backend logs everything to console and `app.log`:
```bash
tail -f app.log       # Linux/macOS
type app.log          # Windows
```

---

## Next Steps

1. ✅ Backend is running
2. Connect frontend to backend API
3. Test the full workflow (upload → analyze → view results)
4. Add Groq API key to your production environment
5. Deploy to production server

---

## Resources

- **Groq API**: https://console.groq.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **API Endpoints**: See README.md for full endpoint documentation
- **Database**: SQLite (policy_bias.db)

---

For detailed documentation, see [README.md](README.md)
