from openai import OpenAI
import json_repair
from flask import current_app

# Example content structure for demonstration
exemple = [
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

def generate_content(domaine, sujet, plan):
    """
    Generate detailed content for each section in the plan
    
    Args:
        domaine: The domain/field (e.g., "Java", "Python", etc.)
        sujet: The specific subject of the presentation
        plan: The presentation plan structure previously generated
        
    Returns:
        A list containing detailed content for each section
    """
    # Get API configuration from Flask config
    api_key = current_app.config['API_KEY']
    base_url = current_app.config['BASE_URL']
    model = current_app.config['MODEL']
    
    content = []
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Process each section in the plan
    for sec in plan.get('sections', []):
        section = sec.get('section')
        sous_sections = sec.get('sous-sections')
        
        # If sous-sections is just a string (like "aucun" for conclusion), make it a list
        if isinstance(sous_sections, str):
            if sous_sections.lower() == "aucun":
                sous_sections = ["Conclusion"]
            else:
                sous_sections = [sous_sections]
        
        # Build the prompt for this section
        prompt = f"""
        Tu es un formateur expert en {domaine}.
        Ton objectif est de générer le contenu pédagogique détaillé pour la section suivante d'une présentation sur le sujet {sujet}.

        Voici la section à développer :
          {section} :

            Sous Sections : {" // ".join(sous_sections) if isinstance(sous_sections, list) else sous_sections}

        Pour chaque sous-section (sauf conclusion) :

        Rédige une explication détaillée de tous les concepts d'une façon claire et progressive.

        Ajoute si nécessaire des exemples bien commentés.

        Utilise si nécessaire des tableaux ou illustrations pour synthétiser les concepts.

        Le contenu doit être structuré en JSON. Commence à générer le JSON directement sans ajouter d'autre message.
        
        Voici un exemple de résultat attendu : {exemple}
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
            section_content = json_repair.loads(response_text)
            content.append(section_content)
        except Exception as e:
            print(f"Error parsing JSON for section '{section}': {str(e)}")
            print(f"Raw response: {response_text}")
            # Add a basic structure to avoid breaking the application
            content.append({
                "title": section,
                "subsections": [
                    {
                        "title": subsection,
                        "content": "Contenu non disponible. Erreur lors de la génération."
                    } for subsection in sous_sections if isinstance(sous_sections, list)
                ]
            })
    
    return content