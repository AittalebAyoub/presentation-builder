# app/utils/quiz_validators.py
from jsonschema import validate, ValidationError

def validate_quiz_data(quiz_data):
    """
    Validate quiz data against the schema
    
    Args:
        quiz_data: Quiz data in JSON format
        
    Returns:
        bool: True if valid, False otherwise
        str: Error message if invalid
    """
    quiz_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "choix_1": {"type": "string"},
                "choix_2": {"type": "string"},
                "choix_3": {"type": "string"},
                "reponse": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1
                }
            },
            "required": ["question", "choix_1", "choix_2", "choix_3", "reponse"]
        }
    }
    
    try:
        validate(instance=quiz_data, schema=quiz_schema)
        return True, ""
    except ValidationError as e:
        return False, str(e)