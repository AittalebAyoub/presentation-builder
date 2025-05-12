# app/services/content_jour_generator.py
from openai import OpenAI
import json_repair
from flask import current_app

# Example content structure for demonstration
exemple_contenu = [
    {
        "title": "Introduction à Python",
        "subsections": [
            {
                "title": "Définition de Python",
                "content": "Python est un langage interprété, multi-paradigme et open-source.",
                "bullets": [
                    "Lisibilité",
                    "Typage dynamique"
                ]
            },
            {
                "title": "Domaines d'application",
                "content": "Python est utilisé dans de nombreux domaines.",
                "table": [
                    ["Domaine", "Exemples d'outils"],
                    ["Data Science", "Pandas, NumPy"],
                    ["Web", "Django, Flask"],
                    ["Intelligence Artificielle", "TensorFlow, Keras"]
                ]
            }
        ]
    }
]

def generate_content_jour(domaine, sujet, plan_jour):
    """
    Generate detailed content for each session in the daily plan
    
    Args:
        domaine: The domain/field (e.g., "Java", "Python", etc.)
        sujet: The specific subject of the presentation
        plan_jour: The daily presentation plan structure previously generated
        
    Returns:
        A list containing detailed content for each day, with each day containing sessions
    """
    # Get API configuration from Flask config
    api_key = current_app.config['API_KEY']
    base_url = current_app.config['BASE_URL']
    model = current_app.config['MODEL']
    
    all_days_content = []
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Process each day in the plan
    for day in plan_jour:
        day_number = day.get('jour')
        sessions = day.get('sessions', [])
        
        day_content = []
        
        # Process each session for this day
        for session in sessions:
            session_title = session.get('title')
            subsections = session.get('subsections', [])
            
            # Build the prompt for this session
            prompt = f"""
            Tu es un formateur expert en {domaine}.
            Ton objectif est de générer le contenu pédagogique détaillé pour la session suivante, qui fait partie du jour {day_number} d'une présentation sur le sujet {sujet}.

            Voici la session à développer :
              Session : {session_title}

              Sous-sections : {", ".join(subsections) if isinstance(subsections, list) else subsections}

            Pour chaque sous-section :
            1. Rédige une explication détaillée de tous les concepts d'une façon claire et progressive.
            2. Ajoute des exemples bien commentés quand c'est pertinent.
            3. Utilise des tableaux pour synthétiser les informations complexes.
            4. Si applicable, inclus des points clés sous forme de liste à puces.
            5. Pour les sujets techniques, ajoute des exemples de code quand c'est approprié.

            Le contenu doit être structuré en JSON selon le format suivant. Commence à générer le JSON directement sans ajouter d'autre message.
            
            Voici un exemple de résultat attendu : {exemple_contenu}
            ```json
            """
            
            # Get the response
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # Lower temperature for more focused output
                top_p=0.9,
            )
            
            # Process the response
            response_text = response.choices[0].message.content
            response_text = response_text.replace("```", "").replace("json", "").strip()
            
            try:
                session_content = json_repair.loads(response_text)
                day_content.append(session_content)
            except Exception as e:
                print(f"Error parsing JSON for session '{session_title}' on day {day_number}: {str(e)}")
                print(f"Raw response: {response_text}")
                # Add a basic structure to avoid breaking the application
                day_content.append({
                    "title": session_title,
                    "subsections": [
                        {
                            "title": subsection,
                            "content": "Contenu non disponible. Erreur lors de la génération."
                        } for subsection in subsections if isinstance(subsections, list)
                    ]
                })
        
        all_days_content.append(day_content)
    
    return all_days_content