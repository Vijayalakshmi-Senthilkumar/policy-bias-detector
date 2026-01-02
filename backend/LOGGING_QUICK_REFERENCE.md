# Logging Quick Reference

## Quick Start

### Run with Debug Logging
```bash
cd backend
export LOG_LEVEL=DEBUG
python main.py
```

### Monitor LLM Operations
Watch for these key log messages:
1. `INFO: Starting policy analysis with Groq API`
2. `INFO: Groq API call completed successfully`
3. `INFO: Policy analysis completed. Found X bias instances`

### Monitor Authentication
Watch for these key log messages:
1. `INFO: Signup request received` / `INFO: Login request received`
2. `INFO: JWT token generated successfully for user`
3. `INFO: Token authentication successful for user`

### Monitor File Processing
Watch for these key log messages:
1. `INFO: Received analysis request`
2. `DEBUG: Processing file upload` / `DEBUG: Processing JSON request body`
3. `INFO: File parsed successfully` / `INFO: File parsed successfully`

---

## Log Format

All logs follow this format:
```
[TIMESTAMP] - [LOGGER_NAME] - [LEVEL] - [MESSAGE]
```

Example:
```
2024-01-02 10:30:45,123 - app.services.groq_service - INFO - Starting policy analysis with Groq API (model: gpt-4-mini)
```

---

## Frequently Used Log Messages

### Success Indicators
✅ `Groq client initialized with model`
✅ `User registered successfully`
✅ `JWT token generated successfully`
✅ `Analysis saved to database`
✅ `File parsed successfully`
✅ `Token verified successfully`

### Error Indicators
❌ `GROQ_API_KEY environment variable is not set`
❌ `Failed to parse Groq response as JSON`
❌ `Failed to initialize database`
❌ `Error during policy analysis`
❌ `Invalid email or password`

### Warning Indicators
⚠️ `Direct JSON parsing failed`
⚠️ `Failed to extract text from PDF page`
⚠️ `User already exists`
⚠️ `Token has expired`

---

## Enabling Verbose Output

### Method 1: Environment Variable
```bash
export LOG_LEVEL=DEBUG
python main.py
```

### Method 2: Configuration
Edit `.env` file:
```
LOG_LEVEL=DEBUG
```

---

## Filtering Logs

### View Only Groq Service Logs
```bash
python main.py 2>&1 | grep "groq_service"
```

### View Only Error Logs
```bash
python main.py 2>&1 | grep "ERROR"
```

### View Analysis Flow
```bash
python main.py 2>&1 | grep "analysis"
```

---

## Common Issues & Log Messages

| Issue | Log Message | Solution |
|-------|-------------|----------|
| API Key Missing | `GROQ_API_KEY environment variable is not set` | Set GROQ_API_KEY in .env |
| JSON Parse Error | `Failed to parse Groq response as JSON` | Check LLM output format |
| File Too Large | `File size exceeds limit` | Reduce file size |
| Invalid Token | `Token has expired` | Generate new token |
| User Exists | `User with this email already exists` | Use different email |
| DB Error | `Failed to initialize database` | Check database connection |

---

## Performance Insights from Logs

### Time LLM Response
```
[TIMESTAMP1] INFO: Starting policy analysis with Groq API
[TIMESTAMP2] INFO: Groq API call completed successfully
```
Response time = TIMESTAMP2 - TIMESTAMP1

### Time File Parsing
```
[TIMESTAMP1] DEBUG: Processing file upload
[TIMESTAMP2] INFO: File parsed successfully
```
Parse time = TIMESTAMP2 - TIMESTAMP1

### Time Database Save
```
[TIMESTAMP1] DEBUG: Saving analysis to database
[TIMESTAMP2] INFO: Analysis saved to database
```
Save time = TIMESTAMP2 - TIMESTAMP1

---

## Debug Checklist

When debugging, verify:
- [ ] Is `GROQ_API_KEY` set? (check for "GROQ_API_KEY found" message)
- [ ] Does LLM respond? (check for "Groq API call completed" message)
- [ ] Is JSON valid? (check for "Direct JSON parsing successful" message)
- [ ] Is data saved? (check for "Analysis saved to database" message)
- [ ] Is auth working? (check for "Token verified successfully" message)

---

## Example Debug Session

### Normal Flow
```
INFO: Received analysis request
DEBUG: Processing JSON request body
DEBUG: Policy name: Test Policy, text length: 1000 characters
INFO: Starting bias analysis for policy: Test Policy
INFO: Starting policy analysis with Groq API (model: gpt-4-mini)
INFO: Groq API call completed successfully
DEBUG: Raw Groq response length: 2000 characters
DEBUG: Starting response parsing...
DEBUG: Direct JSON parsing successful
INFO: Policy analysis completed. Found 5 bias instances
DEBUG: Saving analysis to database...
INFO: Analysis saved to database - ID: abc123
```

### Error Flow (Missing API Key)
```
ERROR: GROQ_API_KEY environment variable is not set!
[ERROR TRACEBACK]
```

### Error Flow (Invalid JSON)
```
INFO: Starting policy analysis with Groq API
INFO: Groq API call completed successfully
DEBUG: Raw Groq response: "invalid json response"
WARNING: Direct JSON parsing failed: ...
ERROR: Failed to parse Groq response as JSON
```

---

## Log Level Recommendations

| Environment | Level | Use Case |
|-------------|-------|----------|
| Local Development | DEBUG | Full visibility, debugging |
| Testing | DEBUG | Test debugging, investigation |
| Staging | INFO | Monitor, catch issues |
| Production | INFO | Performance, minimal overhead |
| Production Emergency | DEBUG | Troubleshoot critical issues |

---

## Integration with Tools

### Python `logging` module
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Message with %s", variable)
logger.debug(f"Formatted message: {variable}")
logger.error("Error occurred", exc_info=True)  # Include traceback
```

### Environment Variables
```bash
# .env file
LOG_LEVEL=DEBUG
LOG_FILE=/var/log/app.log
```

### Configuration
```python
# app/config/config.py
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', None)
```

---

## Tips & Tricks

1. **Use grep to find specific operations**
   ```bash
   python main.py 2>&1 | grep "user_id"
   ```

2. **Save logs to file for later analysis**
   ```bash
   python main.py > /tmp/backend.log 2>&1
   tail -f /tmp/backend.log
   ```

3. **Filter by timestamp to find slow operations**
   ```bash
   # Find operations taking >5 seconds
   python main.py 2>&1 | grep -E "Starting|completed"
   ```

4. **Search for specific user activities**
   ```bash
   python main.py 2>&1 | grep "user_email@example.com"
   ```

5. **Monitor API calls in real-time**
   ```bash
   python main.py 2>&1 | grep -E "Received|request|endpoint"
   ```

---

## Logs Cheat Sheet

```bash
# Debug LLM issues
python main.py 2>&1 | grep -i "groq"

# Debug file parsing
python main.py 2>&1 | grep -i "parse\|file"

# Debug auth issues
python main.py 2>&1 | grep -i "token\|auth\|login\|signup"

# Debug database
python main.py 2>&1 | grep -i "database\|query\|commit"

# View all errors
python main.py 2>&1 | grep "ERROR"

# View all warnings
python main.py 2>&1 | grep "WARNING"

# View startup logs
python main.py 2>&1 | head -30
```

---

## Still Need Help?

Check these locations:
1. **Service logs**: `app/services/*.py` - Service-specific logs
2. **Route logs**: `app/routes/*.py` - API endpoint logs
3. **Startup logs**: `main.py` - Application initialization
4. **Full documentation**: `LOGGING_DOCUMENTATION.md` - Complete reference

---

Last Updated: 2024-01-02
Logging Version: 1.0
