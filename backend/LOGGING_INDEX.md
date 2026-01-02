# Logging Documentation Index

## Quick Navigation

### 🚀 Getting Started
- **New to logging?** Start with [LOGGING_QUICK_REFERENCE.md](LOGGING_QUICK_REFERENCE.md)
- **Want complete details?** See [LOGGING_DOCUMENTATION.md](LOGGING_DOCUMENTATION.md)
- **Curious about implementation?** Check [LOGGING_IMPLEMENTATION_REPORT.md](LOGGING_IMPLEMENTATION_REPORT.md)

---

## 📚 Documentation Files

### 1. LOGGING_QUICK_REFERENCE.md
**Best for**: Quick lookup and common tasks

Contains:
- Quick start (5 minutes to debug logs)
- Frequent log patterns
- Common issues and solutions
- Filtering techniques
- Example debug sessions
- One-liner commands
- Quick checklists

**Start here if**: You need to solve a problem quickly

**Time to read**: 5-10 minutes

---

### 2. LOGGING_DOCUMENTATION.md
**Best for**: Deep understanding and troubleshooting

Contains:
- Complete log reference by service
- Every log message documented
- Log level strategy explained
- Debug workflows step-by-step
- Performance monitoring guide
- Troubleshooting examples
- Integration patterns

**Start here if**: You're debugging a complex issue

**Time to read**: 20-30 minutes

---

### 3. LOGGING_IMPLEMENTATION_REPORT.md
**Best for**: Understanding what was implemented

Contains:
- Implementation summary
- File-by-file changes
- Log distribution metrics
- Real-world examples
- Configuration details
- Best practices
- Next steps

**Start here if**: You want to understand the changes

**Time to read**: 10-15 minutes

---

### 4. LOGGING_SUMMARY.md
**Best for**: High-level overview

Contains:
- What was added
- Files modified list
- Total logging statistics
- Key benefits
- Usage examples
- Summary

**Start here if**: You want a 5-minute overview

**Time to read**: 5 minutes

---

## 🎯 Common Tasks

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python main.py
```
**Reference**: LOGGING_QUICK_REFERENCE.md → "Quick Start"

### Monitor LLM Operations
```bash
python main.py 2>&1 | grep "groq"
```
**Reference**: LOGGING_QUICK_REFERENCE.md → "Logs Cheat Sheet"

### Debug File Upload Issues
Look for these logs in order:
1. "Received analysis request"
2. "Processing file upload"
3. "File received: [filename]"
4. "Parsing file with extension"
5. "File parsed successfully"

**Reference**: LOGGING_DOCUMENTATION.md → "Route-Level Logging"

### Investigate Authentication Failures
Look for these logs:
1. "Signup request received" / "Login request received"
2. "Checking if user exists" / "Querying database for user"
3. "JWT token generated successfully"
4. "Token authentication successful"

**Reference**: LOGGING_DOCUMENTATION.md → "6. Auth Routes"

### Check API Health
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Watch logs for response
python main.py 2>&1 | grep "health"
```
**Reference**: LOGGING_DOCUMENTATION.md → "7. Application Factory"

---

## 📋 Log Levels Reference

| Level | Best For | Use When |
|-------|----------|----------|
| DEBUG | Development, troubleshooting | Need maximum detail |
| INFO | Production, general monitoring | Need overview |
| WARNING | Error recovery, edge cases | Unexpected but handled |
| ERROR | Failures, exceptions | Critical failures occur |

**Reference**: LOGGING_DOCUMENTATION.md → "Log Levels" section

---

## 🔍 Troubleshooting Quick Map

| Problem | Log to Check | File |
|---------|-------------|------|
| API Key Missing | "GROQ_API_KEY not set" | groq_service.py |
| JSON Parse Error | "Failed to parse Groq response" | groq_service.py |
| File Upload Fails | "Error parsing [format] file" | document_parser.py |
| Auth Fails | "Token authentication check" | auth_service.py |
| User Registration Fails | "Error during signup" | auth_routes.py |
| Policy Analysis Fails | "Error during policy analysis" | analysis_routes.py |

**Reference**: LOGGING_QUICK_REFERENCE.md → "Common Issues"

---

## 💡 Pro Tips

### 1. Use grep for filtering
```bash
# Monitor LLM only
python main.py 2>&1 | grep "groq"

# Monitor errors only
python main.py 2>&1 | grep "ERROR"

# Monitor specific user
python main.py 2>&1 | grep "user@example.com"
```

### 2. Save logs for analysis
```bash
python main.py > backend.log 2>&1
tail -f backend.log
```

### 3. Search for specific operations
```bash
# Find all policy analyses
python main.py 2>&1 | grep "Starting policy analysis"

# Find all failed operations
python main.py 2>&1 | grep -E "ERROR|FAILED|failed"
```

### 4. Monitor timing
```bash
# Find slow operations
python main.py 2>&1 | grep -E "Starting|completed"
```

**Reference**: LOGGING_QUICK_REFERENCE.md → "Tips & Tricks"

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Log Statements Added | 250+ |
| Files Modified | 8 |
| Documentation Pages | 4 |
| Lines of Documentation | 1600+ |
| Services with Full Logging | 8/8 |

**Reference**: LOGGING_IMPLEMENTATION_REPORT.md → "Key Metrics"

---

## 🔧 Configuration

### Environment Variables
```bash
# Set log level
export LOG_LEVEL=DEBUG    # DEBUG, INFO, WARNING, ERROR

# Set log file (optional)
export LOG_FILE=/var/log/backend.log
```

### Configuration File (.env)
```
# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=DEBUG

# Optional: log file path
LOG_FILE=/var/log/app.log
```

**Reference**: LOGGING_DOCUMENTATION.md → "Environment Configuration"

---

## 📖 File-by-File Guide

### Services
- **groq_service.py** → LOGGING_DOCUMENTATION.md section "1. Groq LLM Service"
- **bias_detection_service.py** → LOGGING_DOCUMENTATION.md section "2. Bias Detection Service"
- **auth_service.py** → LOGGING_DOCUMENTATION.md section "3. Authentication Service"
- **document_parser.py** → LOGGING_DOCUMENTATION.md section "4. Document Parser Service"

### Routes
- **analysis_routes.py** → LOGGING_DOCUMENTATION.md section "5. Analysis Routes"
- **auth_routes.py** → LOGGING_DOCUMENTATION.md section "6. Auth Routes"

### Core
- **__init__.py** → LOGGING_DOCUMENTATION.md section "7. Application Factory"
- **main.py** → LOGGING_DOCUMENTATION.md section "8. Main Entry Point"

---

## 🎓 Learning Path

### Beginner (5 minutes)
1. Read: LOGGING_QUICK_REFERENCE.md
2. Run: `export LOG_LEVEL=DEBUG && python main.py`
3. Try: Grep for a specific service

### Intermediate (20 minutes)
1. Read: LOGGING_SUMMARY.md
2. Read: LOGGING_QUICK_REFERENCE.md completely
3. Try: Monitor different operations
4. Debug: A simple issue using logs

### Advanced (1 hour)
1. Read: LOGGING_IMPLEMENTATION_REPORT.md
2. Read: LOGGING_DOCUMENTATION.md sections for each service
3. Try: Debug a complex issue
4. Try: Add custom logging to new code
5. Understand: Entire logging architecture

---

## 🆘 Still Confused?

### "Which file should I read?"
- **Quick answer needed?** → LOGGING_QUICK_REFERENCE.md
- **Investigating issue?** → LOGGING_DOCUMENTATION.md
- **Understanding changes?** → LOGGING_IMPLEMENTATION_REPORT.md

### "How do I find a specific log?"
1. Know the operation (e.g., "LLM analysis")
2. Find the section (e.g., "Groq LLM Service")
3. Search for the log message
4. Reference: LOGGING_DOCUMENTATION.md

### "How do I filter logs?"
- Monitor a service: `grep "service_name"`
- Find errors: `grep "ERROR"`
- Find warnings: `grep "WARNING"`
- Find specific user: `grep "email@example.com"`

Reference: LOGGING_QUICK_REFERENCE.md → "Logs Cheat Sheet"

---

## 📝 Example Usage

### Monitor Policy Analysis
```bash
# Terminal 1: Run backend with debug logging
export LOG_LEVEL=DEBUG
python main.py

# Terminal 2: In another terminal, test analysis
curl -X POST http://localhost:5000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"policyText": "We need strong young men", "policyName": "Test"}'

# In Terminal 1, watch the logs show:
# - Request reception
# - LLM API call
# - Response parsing
# - Bias detection
# - Database storage
```

### Monitor User Authentication
```bash
# Watch signup and login flow
python main.py 2>&1 | grep -E "signup|login|token"

# In another terminal:
# 1. Create new user
# 2. Login
# 3. Access protected endpoints
```

---

## 🔗 Cross-References

### For LLM Debugging
- See: LOGGING_DOCUMENTATION.md → "1. Groq LLM Service"
- Also: LOGGING_IMPLEMENTATION_REPORT.md → "1. Groq LLM Service (60+ logs)"

### For Authentication Issues
- See: LOGGING_DOCUMENTATION.md → "3. Authentication Service"
- Also: LOGGING_DOCUMENTATION.md → "6. Auth Routes"

### For File Processing
- See: LOGGING_DOCUMENTATION.md → "4. Document Parser Service"
- Also: LOGGING_DOCUMENTATION.md → "5. Analysis Routes"

### For Database Operations
- See: LOGGING_DOCUMENTATION.md → "5. Analysis Routes"
- Also: LOGGING_DOCUMENTATION.md → "6. Auth Routes"

---

## 💾 File Locations

All documentation files are in the `backend/` directory:

```
backend/
├── LOGGING_QUICK_REFERENCE.md       ← Start here for quick help
├── LOGGING_DOCUMENTATION.md         ← Complete reference
├── LOGGING_SUMMARY.md               ← Overview
├── LOGGING_IMPLEMENTATION_REPORT.md ← Implementation details
├── LOGGING_INDEX.md                 ← This file
└── app/
    ├── services/
    │   ├── groq_service.py          (60+ logs)
    │   ├── bias_detection_service.py (30+ logs)
    │   ├── auth_service.py          (35+ logs)
    │   └── document_parser.py       (25+ logs)
    ├── routes/
    │   ├── analysis_routes.py       (40+ logs)
    │   └── auth_routes.py           (30+ logs)
    └── __init__.py                  (20+ logs)
```

---

## 🎉 Summary

You now have access to:
- ✅ Complete logging documentation
- ✅ Quick reference guides
- ✅ Implementation details
- ✅ Troubleshooting guides
- ✅ Real-world examples

**Next Step**: Pick a documentation file based on your needs and start reading!

---

**Last Updated**: January 2, 2026
**Documentation Version**: 1.0
**Status**: ✅ Complete
