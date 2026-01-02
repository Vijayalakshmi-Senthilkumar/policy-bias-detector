#!/bin/bash
# Backend startup script for Linux/macOS

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Policy Bias Detector - Backend Startup${NC}"
echo "========================================"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓ $python_version${NC}"
else
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install requirements
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠ Please edit .env and add your GROQ_API_KEY${NC}"
    echo -e "${RED}⚠ Then run this script again${NC}"
    exit 1
fi

# Check GROQ_API_KEY
source .env
if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_groq_api_key_here" ]; then
    echo -e "${RED}✗ GROQ_API_KEY is not set in .env${NC}"
    echo -e "${YELLOW}Get your API key from: https://console.groq.com/keys${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration is valid${NC}"

# Start the application
echo ""
echo -e "${GREEN}Starting Policy Bias Detector Backend...${NC}"
echo "========================================"
echo -e "${YELLOW}API Server: http://localhost:5000${NC}"
echo -e "${YELLOW}Health Check: http://localhost:5000/api/health${NC}"
echo ""

python main.py
