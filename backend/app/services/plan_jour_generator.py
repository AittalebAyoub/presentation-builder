# app/services/plan_jour_generator.py

from openai import OpenAI
import json_repair
from flask import current_app

# Example daily plan template for demonstration
exemple_plan_jour = [
  {
    "jour": 1,
    "sessions": [
      {
        "title": "Introduction au Machine Learning",
        "subsections": [
          "Définition du Machine Learning",
          "Importance et applications",
          "Différence avec la programmation traditionnelle"
        ]
      },
      {
        "title": "Types de Machine Learning",
        "subsections": [
          "Tableau des types principaux",
          "Exemples concrets"
        ]
      }
    ]
  },
  {
    "jour": 2,
    "sessions": [
      {
        "title": "Étapes clés du développement d'un modèle",
        "subsections": [
          "Collecte des données",
          "Prétraitement",
          "Entraînement",
          "Évaluation",
          "Déploiement"
        ]
      }
    ]
  }
]

def text_to_json(text):
    """Convert text response from LLM to JSON object"""
    return json_repair.loads(text.replace("```", "").replace("json", "").strip())

def generate_plan_jour(domaine, sujet, description_sujet, niveau_apprenant, nombre_jours):
    """
    Generate a structured presentation plan organized by days based on given parameters
    
    Args:
        domaine: The domain/field (e.g., "Java", "Python", etc.)
        sujet: The specific subject of the presentation
        description_sujet: A detailed description of what should be covered
        niveau_apprenant: The audience level (e.g., "Débutants", "Avancé", etc.)
        nombre_jours: Number of days for the course (integer)
        
    Returns:
        A structured daily plan as a Python list of dictionaries
    """
    # Get API configuration from Flask config
    api_key = current_app.config['API_KEY']
    base_url = current_app.config['BASE_URL']
    model = current_app.config['MODEL']
    
    # Create client
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Build the prompt
    prompt = f"""
    Tu es un formateur expert en {domaine}. Ton objectif est de générer un plan de présentation détaillé 
    et pédagogique sur le sujet suivant : {sujet}, organisé sur {nombre_jours} jours de formation.
    
    Description du sujet : {description_sujet}

    Ce plan est destiné à des apprenants de niveau {niveau_apprenant} en {domaine}.

    Ce plan doit comporter :
      - Une organisation par jours (de 1 à {nombre_jours})
      - Pour chaque jour, plusieurs sessions principales clairement définies
      - Pour chaque session, des sous-sections sous forme de guidelines détaillées, spécifiques et pertinentes
      - Le contenu doit être progressif, pédagogique et adapté au niveau des apprenants
      - La répartition des sessions doit être équilibrée sur les {nombre_jours} jours

    N'intègre pas encore le contenu complet de la présentation, uniquement le plan détaillé 
    avec les titres des sessions et sous-sections.

    Le contenu doit être structuré exactement selon ce format JSON :
    [
      {{
        "jour": 1,
        "sessions": [
          {{
            "title": "Titre de la session 1",
            "subsections": ["Sous-section 1", "Sous-section 2", "Sous-section 3"]
          }},
          {{
            "title": "Titre de la session 2",
            "subsections": ["Sous-section 1", "Sous-section 2"]
          }}
        ]
      }},
      {{
        "jour": 2,
        "sessions": [...]
      }}
    ]

    Exemple de résultat attendu : {exemple_plan_jour}

    Génère une réponse seulement en format JSON. Commence à générer le JSON directement sans ajouter d'autre message.
    
    ```json
    """
    
    # Get the response
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,  # Slightly higher temperature for more creative planning
    )

    # Process the response
    response_text = response.choices[0].message.content
    response_json = text_to_json(response_text)
    return response_json