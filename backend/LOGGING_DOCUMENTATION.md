# Logging Documentation

## Overview

Comprehensive logging has been added throughout the backend system, with a focus on the Groq LLM integration and all critical operations. This documentation outlines all logging points and how to use them for debugging and monitoring.

## Log Levels

The application uses standard Python logging levels:
- **DEBUG**: Detailed information for diagnosing problems (variable values, intermediate steps)
- **INFO**: General informational messages (process starts/completions, key decisions)
- **WARNING**: Warning messages (unexpected conditions, deprecated usage)
- **ERROR**: Error messages (failures, exceptions)

## Environment Configuration

Set the log level via environment variables or config:

```bash
# .env file
LOG_LEVEL=DEBUG    # For development
LOG_LEVEL=INFO     # For production
```

## Service-Level Logging

### 1. Groq LLM Service (`app/services/groq_service.py`)

#### GroqService Initialization
```
INFO: Initializing GroqService...
DEBUG: GROQ_API_KEY found, length: X characters
INFO: Groq client initialized with model: gpt-4-mini
DEBUG: System prompt generated, length: X characters
```

#### Policy Analysis
```
INFO: Starting policy analysis with Groq API (model: gpt-4-mini)
DEBUG: Policy text length: X characters
DEBUG: Policy text preview: [first 200 characters]...
DEBUG: Sending request to Groq API with temperature=0.3, max_tokens=4096
INFO: Groq API call completed successfully
DEBUG: Response object: {...}
DEBUG: Raw Groq response length: X characters
DEBUG: Raw Groq response: {...}
INFO: Policy analysis completed. Found X bias instances
DEBUG: Summary: {...}
```

#### Response Parsing
```
DEBUG: Starting response parsing...
DEBUG: Attempting direct JSON parsing...
DEBUG: Direct JSON parsing successful
WARNING: Direct JSON parsing failed: [error]. Attempting regex extraction...
DEBUG: JSON found in response, attempting to parse...
DEBUG: Regex-extracted JSON parsing successful
DEBUG: Validating response structure...
DEBUG: 'bias_instances' field missing, initializing empty list
DEBUG: 'summary' field missing, generating from bias_instances
DEBUG: Validating X bias instances...
DEBUG: Validating bias instance 0...
DEBUG: Bias instance 0 validated successfully: gender (high)
DEBUG: Response parsing and validation completed successfully
```

#### Bias Instance Validation
```
DEBUG: Validating required fields for bias instance 0...
DEBUG: All required fields present for instance 0
DEBUG: Type validation passed for instance 0: gender
DEBUG: Severity validation passed for instance 0: high
ERROR: Bias instance 0 missing required field: text
ERROR: Bias instance 0 has invalid type: invalid_type
ERROR: Bias instance 0 has invalid severity: invalid_severity
```

#### Summary Generation
```
DEBUG: Generating summary from X bias instances...
DEBUG: Counted gender bias
DEBUG: Counted disability bias
DEBUG: Severity counts - High: 4, Medium: 3, Low: 2
DEBUG: Bias breakdown: {...}
DEBUG: Overall severity determined as 'high' (high_count > 0)
DEBUG: Summary generated: {...}
```

#### Singleton Management
```
INFO: Creating new GroqService singleton instance
DEBUG: Returning existing GroqService singleton instance
```

---

### 2. Bias Detection Service (`app/services/bias_detection_service.py`)

#### Service Initialization
```
INFO: Initializing BiasDetectionService...
DEBUG: BiasDetectionService initialized successfully
```

#### Policy Analysis
```
INFO: Starting bias analysis for policy: [policy_name]
DEBUG: Policy text length: X characters
DEBUG: User ID: [user_id]
DEBUG: Calling GroqService.analyze_policy()...
DEBUG: GroqService.analyze_policy() returned successfully
DEBUG: Creating AnalysisResult object for policy: [policy_name]
DEBUG: AnalysisResult object created with ID: [analysis_id]
DEBUG: Processing X bias instances...
DEBUG: Processing bias instance 0: gender (high)
DEBUG: Bias instance 0 created and appended to analysis
INFO: Analysis completed for policy: [policy_name]
INFO:   Total bias instances: 9
INFO:   Overall severity: high
DEBUG:   Summary: {...}
ERROR: Error during bias analysis for policy '[policy_name]': [error]
```

#### Bias Category Breakdown
```
DEBUG: Calculating bias breakdown by category for analysis ID: [analysis_id]
DEBUG: Counted gender bias instance
DEBUG: Counted disability bias instance
DEBUG: Bias breakdown calculated: {...}
```

---

### 3. Authentication Service (`app/services/auth_service.py`)

#### Token Generation
```
INFO: Generating JWT token for user: [user_id]
DEBUG: Token payload: {...}
DEBUG: JWT secret length: 256 characters
INFO: JWT token generated successfully for user: [user_id]
DEBUG: Token length: 456 characters
ERROR: Error generating JWT token for user [user_id]: [error]
```

#### Token Verification
```
DEBUG: Verifying JWT token, length: 456 characters
INFO: JWT token verified successfully for user: [user_id]
DEBUG: Token payload: {...}
WARNING: JWT token verification failed: Token has expired
WARNING: JWT token verification failed: Invalid token - [error details]
```

#### Token Extraction
```
DEBUG: Extracting token from request headers...
DEBUG: Authorization header found, length: 500 characters
DEBUG: Token extracted successfully, length: 456 characters
WARNING: Token extraction failed: Missing Authorization header
WARNING: Token extraction failed: Invalid Authorization header format. Parts: 1
```

#### Authentication Decorator
```
DEBUG: Token authentication check started...
DEBUG: Extracting token from request...
DEBUG: Verifying token...
INFO: Token authentication successful for user: [user_id]
WARNING: Authentication error: [error message]
ERROR: Unexpected error during authentication: [error]
```

---

### 4. Document Parser Service (`app/services/document_parser.py`)

#### Text File Parsing
```
DEBUG: Parsing text file, file size: 5000 bytes
INFO: Text file parsed successfully, extracted text length: 4850 characters
ERROR: Failed to decode text file as UTF-8: [error]
```

#### PDF File Parsing
```
DEBUG: Parsing PDF file, file size: 50000 bytes
DEBUG: PDF has 5 pages
DEBUG: Extracting text from PDF page 0...
DEBUG: Page 0 extracted, text length: 1200 characters
DEBUG: Extracting text from PDF page 1...
WARNING: Failed to extract text from PDF page 2: [error message]
ERROR: Could not extract any text from PDF
INFO: PDF file parsed successfully, total extracted text length: 5000 characters
ERROR: Error parsing PDF file: [error]
```

#### DOCX File Parsing
```
DEBUG: Parsing DOCX file, file size: 30000 bytes
DEBUG: DOCX has 12 paragraphs
DEBUG: Paragraph 0 extracted, text length: 150 characters
DEBUG: Paragraph 1 extracted, text length: 200 characters
ERROR: Could not extract any text from DOCX
INFO: DOCX file parsed successfully, total extracted text length: 3500 characters
ERROR: Error parsing DOCX file: [error]
```

#### File Routing
```
INFO: Parsing file, type: pdf, size: 50000 bytes
DEBUG: Normalized file type: pdf
DEBUG: Using PDF parser
ERROR: Unsupported file type: xyz
```

#### File Extension Extraction
```
DEBUG: Extracting file extension from filename: policy.pdf
DEBUG: Extracted file extension: pdf
ERROR: Filename has no extension: policy
```

---

## Route-Level Logging

### 5. Analysis Routes (`app/routes/analysis_routes.py`)

#### Analyze Endpoint
```
INFO: Received analysis request
DEBUG: Request method: POST
DEBUG: Request content type: application/json
DEBUG: Authorization header found, attempting to extract user_id...
DEBUG: User authenticated: [user_id]
DEBUG: No authorization header, processing as anonymous user
DEBUG: Processing JSON request body
DEBUG: Policy name: Employee Handbook, text length: 5000 characters
DEBUG: Processing file upload
DEBUG: File received: policy.pdf, size: 50000 bytes
DEBUG: Parsing file with extension: pdf
DEBUG: File parsed successfully, extracted text length: 4850 characters
WARNING: No file provided or empty filename
WARNING: File size exceeds limit: 100000000 > 50000000
ERROR: File parsing error: [error message]
WARNING: Request missing both JSON body and file upload
WARNING: Policy text is empty
WARNING: Policy text exceeds size limit: 1000001 > 1000000 characters
INFO: Starting policy analysis - Name: Employee Handbook, User: [user_id]
DEBUG: Analysis completed successfully - ID: [analysis_id]
DEBUG: Saving analysis to database...
INFO: Analysis saved to database - ID: [analysis_id]
ERROR: Validation error during analysis: [error]
ERROR: Error during policy analysis: [error]
```

#### Get Analysis Endpoint
```
INFO: Retrieving analysis - ID: [analysis_id]
DEBUG: Querying database for analysis ID: [analysis_id]
WARNING: Analysis not found - ID: [analysis_id]
INFO: Analysis found and returning - ID: [analysis_id]
ERROR: Error retrieving analysis: [error]
```

#### Get User Analyses Endpoint
```
INFO: Retrieving analyses for user - ID: [user_id]
DEBUG: Pagination - Page: 1, Per Page: 10
DEBUG: Total analyses for user [user_id]: 15
INFO: Retrieved 10 analyses for user - ID: [user_id]
ERROR: Error retrieving user analyses: [error]
```

#### Delete Analysis Endpoint
```
INFO: Deleting analysis - ID: [analysis_id], User: [user_id]
DEBUG: Querying database for analysis ID: [analysis_id] owned by user: [user_id]
WARNING: Analysis not found or unauthorized - ID: [analysis_id], User: [user_id]
DEBUG: Deleting analysis from database - ID: [analysis_id]
INFO: Analysis deleted successfully - ID: [analysis_id], User: [user_id]
ERROR: Error deleting analysis: [error]
```

---

### 6. Auth Routes (`app/routes/auth_routes.py`)

#### Signup Endpoint
```
INFO: Signup request received
DEBUG: Signup attempt - Email: user@example.com, Name: John Doe
WARNING: Signup validation failed: Missing email, password, or name
WARNING: Signup validation failed: Password too short for email user@example.com
DEBUG: Checking if user exists - Email: user@example.com
WARNING: Signup failed: User already exists - Email: user@example.com
DEBUG: Creating new user - Email: user@example.com, Name: John Doe
DEBUG: Hashing password for user - Email: user@example.com
INFO: User registered successfully - Email: user@example.com, ID: [user_id]
DEBUG: Generating JWT token for new user - ID: [user_id]
ERROR: Error during signup: [error]
```

#### Login Endpoint
```
INFO: Login request received
DEBUG: Login attempt - Email: user@example.com
WARNING: Login validation failed: Missing email or password
DEBUG: Querying database for user - Email: user@example.com
WARNING: Login failed: User not found - Email: user@example.com
DEBUG: User found, verifying password - Email: user@example.com
WARNING: Login failed: Invalid password - Email: user@example.com
INFO: User logged in successfully - Email: user@example.com, ID: [user_id]
DEBUG: Generating JWT token for logged-in user - ID: [user_id]
ERROR: Error during login: [error]
```

#### Verify Token Endpoint
```
INFO: Token verification request - User ID: [user_id]
DEBUG: Querying database for user - ID: [user_id]
WARNING: Token verification failed: User not found - ID: [user_id]
INFO: Token verified successfully - User ID: [user_id], Email: user@example.com
ERROR: Error verifying token: [error]
```

---

### 7. Application Factory (`app/__init__.py`)

#### App Creation
```
INFO: Creating Flask app with config: DevelopmentConfig
DEBUG: Config details - ENV: development, DEBUG: True, HOST: 127.0.0.1:5000
DEBUG: Setting up CORS with origins: ['http://localhost:3000', 'http://localhost:5173']
INFO: CORS configured successfully
INFO: Initializing database at: sqlite:///policy_bias_detector.db
INFO: Database initialized successfully
DEBUG: Registering blueprints...
DEBUG: Auth blueprint registered
DEBUG: Analysis blueprint registered
INFO: All blueprints registered successfully
DEBUG: Health check requested
DEBUG: Root endpoint requested
WARNING: 404 error: [endpoint not found]
ERROR: 500 Internal server error: [error details]
INFO: Flask app created and configured successfully
```

---

### 8. Main Entry Point (`main.py`)

#### Application Startup
```
================================================================================
STARTING POLICY BIAS DETECTOR BACKEND
================================================================================
INFO: Configuration loaded successfully
INFO:   Environment: development
INFO:   Debug Mode: True
INFO:   Log Level: DEBUG
INFO:   Database: sqlite:///policy_bias_detector.db
INFO:   Groq Model: gpt-4-mini
INFO: Creating Flask application...
INFO: Flask application created successfully
INFO: Initializing database...
INFO: Database initialized successfully
================================================================================
Flask server starting on 127.0.0.1:5000
API health check: http://127.0.0.1:5000/api/health
API endpoints base: http://127.0.0.1:5000/api
================================================================================
```

---

## Debug Workflow

### Enable Debug Logging
```bash
# Set environment variable
export LOG_LEVEL=DEBUG
python main.py
```

### Common Debugging Scenarios

#### 1. LLM API Issues
Look for logs starting with:
- "Starting policy analysis with Groq API"
- "Groq API call completed successfully"
- "Raw Groq response" (contains the actual LLM output)

#### 2. JSON Parsing Errors
Look for logs:
- "Starting response parsing..."
- "Direct JSON parsing successful/failed"
- "Regex-extracted JSON parsing successful"

#### 3. Authentication Problems
Look for logs:
- "Token authentication check started..."
- "Token verified successfully"
- "Authentication error: Missing Authorization header"

#### 4. Database Issues
Look for logs:
- "Database initialized successfully"
- "Saving analysis to database..."
- "Querying database for..."

#### 5. File Upload Problems
Look for logs:
- "Processing file upload"
- "File received: [filename]"
- "File parsed successfully"

---

## Log File Locations

### Development
Console output only (no file logging)

### Production
Set `LOG_FILE` environment variable:
```bash
export LOG_FILE=/var/log/policy-bias-detector/backend.log
```

---

## Performance Monitoring

Use logs to track performance:

1. **LLM Response Time**: Check time between "Starting policy analysis" and "Policy analysis completed"
2. **File Parsing**: Check time between "Processing file upload" and "File parsed successfully"
3. **Database Operations**: Check time between "Saving analysis to database" and "Analysis saved to database"

---

## Example Log Analysis

### Successful Analysis Flow
```
INFO: Received analysis request
DEBUG: Processing JSON request body
DEBUG: Policy name: Employee Handbook, text length: 5000 characters
INFO: Starting policy analysis for policy: Employee Handbook
INFO: Starting policy analysis with Groq API (model: gpt-4-mini)
DEBUG: Policy text length: 5000 characters
DEBUG: Sending request to Groq API with temperature=0.3, max_tokens=4096
INFO: Groq API call completed successfully
DEBUG: Raw Groq response length: 3000 characters
DEBUG: Starting response parsing...
DEBUG: Direct JSON parsing successful
DEBUG: Validating 9 bias instances...
INFO: Policy analysis completed. Found 9 bias instances
INFO: Analysis completed for policy: Employee Handbook
INFO:   Total bias instances: 9
INFO:   Overall severity: high
DEBUG: Saving analysis to database...
INFO: Analysis saved to database - ID: abc123
```

### Failed Analysis Flow
```
INFO: Received analysis request
ERROR: File parsing error: Could not extract any text from PDF
ERROR: Error during policy analysis: Analysis failed
```

---

## Best Practices

1. **Always check logs when issues occur** - they provide detailed context
2. **Use DEBUG level during development** - provides maximum visibility
3. **Use INFO level in production** - balances visibility with log volume
4. **Monitor exception traces** - use `exc_info=True` captures full stack traces
5. **Include request context** - logs include user IDs, file names, policy names for tracing

---

## Troubleshooting Guide

### Issue: "GROQ_API_KEY not set"
```
Check: "Initializing GroqService..." message
Solution: Set GROQ_API_KEY environment variable
```

### Issue: "Invalid JSON response"
```
Check: "Direct JSON parsing failed" message
Check: "Raw Groq response" to see actual LLM output
Solution: May need to adjust system prompt or temperature settings
```

### Issue: "File parsing failed"
```
Check: "Processing file upload" and "File received" messages
Check: Specific error message in "Error parsing [format] file"
Solution: Verify file format is supported (txt, pdf, docx)
```

### Issue: "Authentication failed"
```
Check: "Extracting token from request headers" message
Check: "Token authentication check started" message
Solution: Ensure Authorization header is properly formatted: "Bearer [token]"
```

---

## Future Enhancements

- [ ] Structured logging (JSON format for log aggregation)
- [ ] Log rotation and retention policies
- [ ] Performance metrics collection
- [ ] Distributed tracing support
- [ ] Real-time log monitoring dashboard
