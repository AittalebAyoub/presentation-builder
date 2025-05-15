from openai import OpenAI
import json_repair
from flask import current_app

# Example plan template for demonstration
exemple_plan = {
  "titre": "Les Bases de PYTHON pour Débutants",
  "sections": [
    {
      "section": "Introduction à Python",
      "sous-sections": [
        "Qu'est-ce que Python ?",
        "Pourquoi apprendre Python ?",
        "Installation de Python et configuration de l'environnement",
        "Premier programme : 'Hello, World!'"
      ]
    },
    {
      "section": "Les Fondamentaux de Python",
      "sous-sections": [
        "Les variables et les types de données",
        "Les opérateurs (arithmétiques, de comparaison, logiques)",
        "Les structures de contrôle (if, else, elif)",
        "Les boucles (for, while)"
      ]
    },
    {
      "section": "Conclusion",
      "sous-sections": "aucun"
    }
  ]
}

def text_to_json(text):
    """Convert text response from LLM to JSON object"""
    return json_repair.loads(text.replace("```", "").replace("json", "").strip())

def generate_plan(domaine, sujet, description_sujet, niveau_apprenant):
    """
    Generate a structured presentation plan based on given parameters
    
    Args:
        domaine: The domain/field (e.g., "Java", "Python", etc.)
        sujet: The specific subject of the presentation
        description_sujet: A detailed description of what should be covered
        niveau_apprenant: The audience level (e.g., "Débutants", "Avancé", etc.)
        
    Returns:
        A structured plan as a Python dictionary
    """
    # Get API configuration from Flask config
    api_key = current_app.config['API_KEY']
    base_url = current_app.config['BASE_URL']
    model = current_app.config['MODEL']
    
    # Create client
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Build the prompt
    prompt = f"""
    Tu es un formateur expert en {domaine}. Ton objectif est de générer un plan de présentation détaillé et pédagogique sur le sujet suivant : {sujet}.
    Description du sujet : {description_sujet}

    Ce plan est destiné à des apprenants de niveau {niveau_apprenant} en programmation.

    Ce plan doit comporter :
          - Des sections principales clairement définies.
          - Pour chaque section, des sous-sections sous forme de guidelines détaillées, spécifiques et pertinentes.
          - Le contenu doit être progressif, pédagogique et adapté au niveau des apprenants.

    N'intègre pas encore le contenu complet de la présentation, uniquement le plan détaillé avec les titres des sections et sous-sections.
    Pour la conclusion, génère la conclusion directement sans ajouter de sous-sections.

    Le contenu doit être structuré en JSON. Commence à générer le JSON directement sans ajouter d'autre message.

    Exemple de résultat attendu : {exemple_plan}

    ```json
    """
    
    # Get the response
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    # Process the response
    response_text = response.choices[0].message.content
    response_json = text_to_json(response_text)
    print(f'Plan : {response_json}')
    return response_json