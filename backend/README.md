# Policy Bias Detector - Backend API

A Python Flask backend for detecting hidden bias in company policies using the Groq LLM API.

## Features

- **AI-Powered Bias Detection**: Uses Groq's high-speed LLM models to analyze policies
- **Multiple Bias Categories**: Detects gender, age, disability, racial, and other biases
- **Document Support**: Parse TXT, PDF, and DOCX files
- **User Authentication**: JWT-based authentication system
- **Database Persistence**: Store and retrieve analysis results
- **REST API**: Clean, RESTful API endpoints
- **CORS Enabled**: Easily integrates with frontend applications

## Architecture

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config/
│   │   └── config.py        # Configuration management
│   ├── models/
│   │   └── models.py        # SQLAlchemy database models
│   ├── services/
│   │   ├── groq_service.py          # Groq API integration
│   │   ├── bias_detection_service.py # Bias analysis logic
│   │   ├── auth_service.py          # JWT authentication
│   │   └── document_parser.py       # File parsing
│   ├── routes/
│   │   ├── auth_routes.py   # Authentication endpoints
│   │   └── analysis_routes.py # Analysis endpoints
│   └── utils/
│       └── helpers.py        # Utility functions
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create from .env.example)
└── .env.example             # Example environment configuration
```

## Requirements

- Python 3.8+
- Groq API Key (get from https://console.groq.com/keys)
- Pip package manager

## Installation

### 1. Clone/Setup Backend Directory

The backend folder should already be created. Navigate to it:

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. Generate JWT secret:
   ```bash
   # Windows PowerShell
   -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

   # Linux/macOS
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

   Add it to `.env`:
   ```
   JWT_SECRET=your_generated_jwt_secret
   ```

### 5. Initialize Database

```bash
python main.py
# The database will be created on first run
```

## Running the Backend

### Development Mode

```bash
python main.py
```

The API will start on `http://127.0.0.1:5000`

### With Custom Configuration

```bash
# Custom port
set FLASK_PORT=8000  # Windows
export FLASK_PORT=8000  # Linux/macOS

# Production mode
set FLASK_ENV=production  # Windows
export FLASK_ENV=production  # Linux/macOS
```

## API Endpoints

### Health Check
- **GET** `/api/health` - Check API status

### Authentication
- **POST** `/api/auth/signup` - User registration
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "name": "User Name"
  }
  ```

- **POST** `/api/auth/login` - User login
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

- **POST** `/api/auth/verify` - Verify token (requires Authorization header)

### Policy Analysis
- **POST** `/api/analysis/analyze` - Analyze policy for bias
  ```json
  {
    "policyText": "Company policy text...",
    "policyName": "Policy Name (optional)"
  }
  ```
  
  Or upload a file (multipart/form-data):
  ```
  file: [binary file]
  policyName: "Policy Name (optional)"
  ```

- **GET** `/api/analysis/<analysis_id>` - Retrieve analysis results

- **GET** `/api/analysis/user/analyses` - Get user's analyses (requires auth)

- **DELETE** `/api/analysis/<analysis_id>` - Delete analysis (requires auth)

## Example Usage

### 1. Register User

```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

### 2. Analyze Policy

```bash
curl -X POST http://localhost:5000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "policyText": "We seek young and energetic candidates who are digital natives...",
    "policyName": "Employee Conduct Policy"
  }'
```

### 3. Upload and Analyze Document

```bash
curl -X POST http://localhost:5000/api/analysis/analyze \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@policy.pdf" \
  -F "policyName=HR Policy"
```

## Groq LLM Integration

### How It Works

1. User submits a policy (text or document)
2. Backend parses the document if needed
3. Policy text is sent to Groq API with a detailed prompt
4. Groq LLM analyzes the policy and identifies bias instances
5. Response is parsed and structured into BiasInstance objects
6. Results are stored in the database
7. Frontend receives the analysis with highlighted biases

### Model Configuration

Default model: `llama-3.3-70b-versatile` (most accurate)

To change the model, edit `app/config/config.py`:
```python
GROQ_MODEL = 'mixtral-8x7b-32768'  # Faster alternative
```

Available models: https://console.groq.com/docs/models

## Database Schema

### Users Table
- `id` (UUID) - Primary key
- `email` (String) - Unique email address
- `password_hash` (String) - Bcrypt hashed password
- `name` (String) - User's name
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### AnalysisResults Table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to Users
- `policy_name` (String) - Name of the policy
- `policy_text` (Text) - Full policy text
- `total_bias_count` (Integer) - Number of bias instances found
- `overall_severity` (String) - low/medium/high
- `analyzed_at` (DateTime) - When analysis was performed
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

### BiasInstances Table
- `id` (UUID) - Primary key
- `analysis_id` (UUID) - Foreign key to AnalysisResults
- `original_text` (String) - The biased text
- `bias_type` (String) - gender/age/disability/racial/other
- `severity` (String) - low/medium/high
- `explanation` (Text) - Why it's biased
- `suggested_rewrite` (String) - Inclusive alternative
- `start_index` (Integer) - Character position in policy
- `end_index` (Integer) - Character position in policy
- `created_at` (DateTime) - Creation timestamp

## Security Considerations

1. **API Keys**: Never commit `.env` file. Use `.env.example` for reference
2. **JWT Tokens**: Tokens expire after 24 hours (configurable)
3. **Password Hashing**: Bcrypt used for password storage
4. **CORS**: Configured for specific origins only
5. **Input Validation**: All inputs are validated
6. **SQL Injection**: SQLAlchemy ORM prevents SQL injection
7. **Rate Limiting**: Can be added for production

## Troubleshooting

### GROQ_API_KEY not set
- Ensure `.env` file exists in the backend directory
- Check that `GROQ_API_KEY` is set with a valid Groq API key

### Database Errors
- Delete `policy_bias.db` and restart to reset the database
- Check database permissions

### CORS Errors
- Update `CORS_ORIGINS` in `.env` to match your frontend URL
- Default: `http://localhost:5173,http://localhost:3000`

### Token Validation Errors
- Ensure token is included in `Authorization: Bearer <token>` header
- Check that token hasn't expired

## Performance Optimization

1. **Caching**: Implement Redis for caching analysis results
2. **Async Processing**: Use Celery for background analysis jobs
3. **Database Indexing**: Indexes on frequently queried fields
4. **Rate Limiting**: Prevent API abuse with rate limiting

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:create_app
```

### Using Docker

See `Dockerfile` for containerization (to be created)

## Contributing

1. Follow PEP 8 style guide
2. Add docstrings to all functions
3. Write unit tests for new features
4. Update README for any changes

## License

[Your License Here]

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Groq API documentation: https://console.groq.com/docs
3. Check Flask documentation: https://flask.palletsprojects.com/

## Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT Specification](https://jwt.io/)
