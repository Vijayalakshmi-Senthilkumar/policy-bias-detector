import json
import logging
from typing import Dict, List, Any
from groq import Groq
from app.config.config import Config

logger = logging.getLogger(__name__)


class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self):
        """Initialize Groq client"""
        logger.info("Initializing GroqService...")
        
        if not Config.GROQ_API_KEY:
            logger.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        logger.debug(f"GROQ_API_KEY found, length: {len(Config.GROQ_API_KEY)} characters")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL
        logger.info(f"Groq client initialized with model: {self.model}")
        
        self.system_prompt = self._get_system_prompt()
        logger.debug(f"System prompt generated, length: {len(self.system_prompt)} characters")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for bias detection"""
        return """You are an expert HR and compliance advisor specializing in identifying biased language in company policies. 
Your task is to analyze policies for discriminatory language and provide structured feedback.

You will identify bias in the following categories:
1. GENDER BIAS: Language that assumes gender or excludes based on gender
2. AGE BIAS: Language that favors or excludes based on age
3. DISABILITY BIAS: Language that excludes people with disabilities or assumes physical/mental capabilities
4. RACIAL/ETHNIC BIAS: Language that favors certain races or ethnicities or uses stereotypes
5. OTHER BIAS: Any other discriminatory language

For each instance of bias found, you MUST respond with a JSON object containing:
- text: The exact problematic text from the policy
- type: One of [gender, age, disability, racial, other]
- severity: One of [low, medium, high]
- explanation: A clear, professional explanation of why this is biased (2-3 sentences)
- suggested_rewrite: A specific, inclusive alternative that maintains the policy's intent

RESPOND ONLY WITH VALID JSON in this format:
{
  "bias_instances": [
    {
      "text": "...",
      "type": "...",
      "severity": "...",
      "explanation": "...",
      "suggested_rewrite": "..."
    }
  ],
  "summary": {
    "total_bias_count": 0,
    "overall_severity": "low",
    "bias_breakdown": {
      "gender": 0,
      "age": 0,
      "disability": 0,
      "racial": 0,
      "other": 0
    }
  }
}

If no bias is found, return an empty bias_instances array but still include the summary with all counts as 0.
"""
    
    def analyze_policy(self, policy_text: str) -> Dict[str, Any]:
        """
        Analyze a policy for bias using Groq API
        
        Args:
            policy_text: The company policy text to analyze
            
        Returns:
            Dictionary containing bias instances and summary
        """
        try:
            logger.info(f"Starting policy analysis with Groq API (model: {self.model})")
            logger.debug(f"Policy text length: {len(policy_text)} characters")
            logger.debug(f"Policy text preview: {policy_text[:200]}...")
            
            # Create the message for Groq API
            messages = [
                {
                    "role": "user",
                    "content": f"""Please analyze the following company policy for biased language and respond with ONLY valid JSON:

POLICY TEXT:
{policy_text}

Remember to respond ONLY with valid JSON, no other text."""
                }
            ]
            
            logger.debug(f"Sending request to Groq API with temperature=0.3, max_tokens=4096")
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=4096,
                system=self.system_prompt,
            )
            
            logger.info("Groq API call completed successfully")
            logger.debug(f"Response object: {chat_completion}")
            
            # Extract the response content
            response_content = chat_completion.choices[0].message.content
            logger.debug(f"Raw Groq response length: {len(response_content)} characters")
            logger.debug(f"Raw Groq response: {response_content}")
            
            # Parse the JSON response
            response_data = self._parse_response(response_content)
            
            bias_count = len(response_data.get('bias_instances', []))
            logger.info(f"Policy analysis completed. Found {bias_count} bias instances")
            logger.debug(f"Summary: {response_data.get('summary', {})}")
            
            return response_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {e}", exc_info=True)
            raise ValueError(f"Invalid JSON response from Groq API: {str(e)}")
        except Exception as e:
            logger.error(f"Error during policy analysis: {str(e)}", exc_info=True)
            raise
    
    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """
        Parse and validate the Groq API response
        
        Args:
            response_content: Raw response from Groq API
            
        Returns:
            Parsed response dictionary
        """
        logger.debug("Parsing Groq API response...")
        
        # Try to find JSON in the response
        try:
            # First try to parse as-is
            response_data = json.loads(response_content)
            logger.debug("Response parsed directly as JSON")
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            logger.debug("Direct parsing failed, attempting to extract from markdown...")
            if '```json' in response_content:
                json_str = response_content.split('```json')[1].split('```')[0].strip()
                response_data = json.loads(json_str)
                logger.debug("JSON extracted from markdown code block")
            elif '```' in response_content:
                json_str = response_content.split('```')[1].split('```')[0].strip()
                response_data = json.loads(json_str)
                logger.debug("JSON extracted from code block")
            else:
                raise ValueError("Could not find valid JSON in response")
        
        # Validate response structure
        logger.debug("Validating response structure...")
        if 'bias_instances' not in response_data:
            logger.warning("Response missing 'bias_instances' field, using empty list")
            response_data['bias_instances'] = []
        
        if 'summary' not in response_data:
            logger.warning("Response missing 'summary' field, generating default")
            response_data['summary'] = self._generate_summary(response_data.get('bias_instances', []))
        
        # Validate and normalize bias instances
        logger.debug(f"Validating {len(response_data['bias_instances'])} bias instances...")
        for index, instance in enumerate(response_data['bias_instances']):
            self._validate_bias_instance(instance, index)
        
        logger.debug("Response validation completed successfully")
        return response_data
    
    def _validate_bias_instance(self, instance: Dict[str, Any], index: int = 0) -> None:
        """
        Validate a bias instance has all required fields
        
        Args:
            instance: The bias instance to validate
            index: The index of this instance in the list
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        logger.debug(f"Validating bias instance {index}...")
        
        required_fields = ['text', 'type', 'severity', 'explanation', 'suggested_rewrite']
        for field in required_fields:
            if field not in instance:
                logger.error(f"Bias instance {index} missing required field: {field}")
                raise ValueError(f"Bias instance {index} missing required field: {field}")
        
        logger.debug(f"All required fields present for instance {index}")
        
        # Validate type
        valid_types = ['gender', 'age', 'disability', 'racial', 'other']
        if instance['type'] not in valid_types:
            logger.error(f"Bias instance {index} has invalid type: {instance['type']}. Valid types: {valid_types}")
            raise ValueError(f"Bias instance {index} has invalid type: {instance['type']}")
        
        logger.debug(f"Type validation passed for instance {index}: {instance['type']}")
        
        # Validate severity
        valid_severities = ['low', 'medium', 'high']
        if instance['severity'] not in valid_severities:
            logger.error(f"Bias instance {index} has invalid severity: {instance['severity']}. Valid severities: {valid_severities}")
            raise ValueError(f"Bias instance {index} has invalid severity: {instance['severity']}")
        
        logger.debug(f"Severity validation passed for instance {index}")
    
    def _generate_summary(self, bias_instances: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary from bias instances
        
        Args:
            bias_instances: List of bias instances found
            
        Returns:
            Summary dictionary
        """
        logger.debug(f"Generating summary from {len(bias_instances)} bias instances...")
        
        bias_breakdown = {
            'gender': 0,
            'age': 0,
            'disability': 0,
            'racial': 0,
            'other': 0,
        }
        
        high_count = 0
        medium_count = 0
        
        for instance in bias_instances:
            bias_type = instance.get('type', 'other')
            if bias_type in bias_breakdown:
                bias_breakdown[bias_type] += 1
                logger.debug(f"Counted {bias_type} bias")
            
            severity = instance.get('severity', 'low')
            if severity == 'high':
                high_count += 1
            elif severity == 'medium':
                medium_count += 1
        
        logger.debug(f"Severity counts - High: {high_count}, Medium: {medium_count}")
        logger.debug(f"Bias breakdown: {bias_breakdown}")
        
        # Determine overall severity
        if high_count > 0:
            overall_severity = 'high'
            logger.debug("Overall severity determined as 'high' (high_count > 0)")
        elif medium_count > 2:
            overall_severity = 'high'
            logger.debug("Overall severity determined as 'high' (medium_count > 2)")
        elif medium_count > 0:
            overall_severity = 'medium'
            logger.debug("Overall severity determined as 'medium'")
        else:
            overall_severity = 'low'
            logger.debug("Overall severity determined as 'low'")
        
        summary = {
            'total_bias_count': len(bias_instances),
            'overall_severity': overall_severity,
            'bias_breakdown': bias_breakdown,
        }
        logger.debug(f"Summary generated: {summary}")
        return summary


# Singleton instance
_groq_service = None


def get_groq_service() -> GroqService:
    """Get or create Groq service instance"""
    global _groq_service
    if _groq_service is None:
        logger.info("Creating new GroqService singleton instance")
        _groq_service = GroqService()
    else:
        logger.debug("Returning existing GroqService singleton instance")
    return _groq_service
