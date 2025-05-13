# app/services/quiz_generator.py
import json
import logging
from openai import OpenAI
from flask import current_app
from app.utils.quiz_validators import validate_quiz_data

# Example quiz data for few-shot learning
FEW_SHOT_EXAMPLES = [
    {
        "question": "Quels éléments sont nécessaires pour définir une fonction en Python ?",
        "choix_1": "Le mot-clé def",
        "choix_2": "Le nom de la fonction",
        "choix_3": "Un point-virgule à la fin",
        "reponse": ["choix_1", "choix_2"]
    },
    {
        "question": "Parmi les types suivants, lesquels sont des types de données standards en Python ?",
        "choix_1": "list",
        "choix_2": "map",
        "choix_3": "dict",
        "reponse": ["choix_1", "choix_3"]
    },
    {
        "question": "Quel mot-clé permet de créer une fonction en Python ?",
        "choix_1": "function",
        "choix_2": "def",
        "choix_3": "fun",
        "reponse": ["choix_2"]
    },
    {
        "question": "Quelles instructions permettent de répéter un bloc de code en Python ?",
        "choix_1": "for",
        "choix_2": "while",
        "choix_3": "loop",
        "reponse": ["choix_1", "choix_2"]
    },
    {
        "question": "Quelles sont les bonnes pratiques pour nommer une variable en Python ?",
        "choix_1": "Utiliser des noms explicites",
        "choix_2": "Commencer par un chiffre",
        "choix_3": "Utiliser des underscores pour séparer les mots",
        "reponse": ["choix_1", "choix_3"]
    },
    {
        "question": "Que renvoie l'instruction print(type(42)) ?",
        "choix_1": "<class 'str'>",
        "choix_2": "<class 'float'>",
        "choix_3": "<class 'int'>",
        "reponse": ["choix_3"]
    }
]

logger = logging.getLogger(__name__)

def create_quiz(content, level="intermediaire", nbr_qst=5):
    """
    Generate quiz questions based on the provided content
    
    Args:
        content: Content to generate quiz questions from
        level: Difficulty level (debutant, intermediaire, avance)
        nbr_qst: Number of questions to generate
        
    Returns:
        list: Generated quiz questions
        str: Error message if any
    """
    # Get API configuration from Flask config
    api_key = current_app.config['API_KEY']
    base_url = current_app.config['BASE_URL']
    model = current_app.config['QUIZ_MODEL']
    
    system_message = """Tu es un assistant pédagogique intelligent spécialisé dans la génération de quiz à partir de contenus 
    de formation. Ton objectif est de générer des questions pertinentes, claires et pédagogiques, adaptées au niveau indiqué 
    (débutant, intermédiaire ou avancé). Tu respectes le format demandé (question à choix unique ou multiple) et le nombre 
    de questions spécifié.
    
    Chaque question doit être suivie de ses choix de réponses, puis de la bonne réponse clairement indiquée.
    Tu évites le contenu flou, répétitif ou hors sujet, et tu t'assures que chaque question teste une notion bien précise 
    du contenu fourni."""
    
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
    
    prompt = f"""
    ### Données d'entrée :
        - **contenu de la formation** : {content}
        - **Niveau de difficulté** : {level}
        - **Nombre des questions** : {nbr_qst}
    
    Le contenu doit être structuré en JSON. Commence à générer le JSON directement sans ajouter d'autre message.
    Voici un exemple de résultat attendu : {FEW_SHOT_EXAMPLES}
    
    La sortie doit être exactement au même format que cet exemple : une seule liste contenant des dictionnaires.
    Voila le schéma d'output que tu dois respecter : {quiz_schema}
    """
    
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # Extract response content
        response_text = response.choices[0].message.content
        
        # Clean response to extract valid JSON
        cleaned_text = response_text.strip()
        
        # If response is wrapped in ```json ``` code blocks, remove them
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.replace("```json", "", 1)
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        
        # Parse JSON
        quiz_data = json.loads(cleaned_text)
        
        # Validate quiz data format
        is_valid, error_message = validate_quiz_data(quiz_data)
        if not is_valid:
            return None, f"Generated quiz data has invalid format: {error_message}"
        
        return quiz_data, None
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Response text: {response_text}")
        return None, f"Failed to parse generated quiz data: {str(e)}"
    except Exception as e:
        logger.error(f"Quiz generation error: {e}")
        return None, f"Failed to generate quiz: {str(e)}"