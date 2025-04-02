import os
import json
import logging
from flask import current_app

def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def save_to_json(data, filename, directory=None):
    """Save data to a JSON file."""
    if directory is None:
        directory = current_app.config['OUTPUT_FOLDER']
    
    ensure_dir(directory)
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath

def load_from_json(filename, directory=None):
    """Load data from a JSON file."""
    if directory is None:
        directory = current_app.config['OUTPUT_FOLDER']
    
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                'app.log'
            ))
        ]
    )
    return logging.getLogger('app')

def get_file_extension(filename):
    """Get the extension of a file."""
    return os.path.splitext(filename)[1].lower()[1:]

# Add this to your app/utils/helpers.py file
def text_to_safe_filename(text):
    """Convert any text to a safe filename."""
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Remove any characters that are not alphanumeric, underscore, or hyphen
    text = ''.join(c for c in text if c.isalnum() or c in ['_', '-'])
    # Ensure it's not too long
    if len(text) > 100:
        text = text[:100]
    # Return the safe filename
    return text