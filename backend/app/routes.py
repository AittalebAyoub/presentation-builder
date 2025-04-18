from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
import time
import traceback
from werkzeug.utils import secure_filename

from app.services.plan_jour_generator import generate_plan_jour

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

# Import service functions (these will be implemented in the services files)
from app.services.plan_generator import generate_plan
from app.services.content_generator import generate_content
from app.services.pdf_generator import create_pdf
from app.services.pptx_generator import generate_powerpoint

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads (for logos, etc.)."""
    # Check if file part exists in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if the file type is allowed
    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        # Create a unique filename to prevent overwriting
        unique_filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)
        return jsonify({
            'success': True, 
            'filename': unique_filename,
            'filepath': filepath
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@main.route('/api/generate-plan', methods=['POST'])
def api_generate_plan():
    """Generate a presentation plan based on provided parameters."""
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract required parameters
        domaine = data.get('domaine')
        sujet = data.get('sujet')
        description_sujet = data.get('description_sujet', '')
        niveau_apprenant = data.get('niveau_apprenant')
        
        # Validate required parameters
        if not all([domaine, sujet, niveau_apprenant]):
            return jsonify({'error': 'Missing required fields: domaine, sujet, niveau_apprenant'}), 400
        
        # Generate the plan
        start_time = time.time()
        plan = generate_plan(domaine, sujet, description_sujet, niveau_apprenant)
        execution_time = round(time.time() - start_time, 2)
        
        # Return the plan with timing information
        return jsonify({
            'success': True,
            'execution_time_seconds': execution_time,
            'plan': plan
        })
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating plan: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to generate plan: {str(e)}'}), 500

@main.route('/api/generate-content', methods=['POST'])
def api_generate_content():
    """Generate presentation content based on the provided plan."""
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract required parameters
        domaine = data.get('domaine')
        sujet = data.get('sujet')
        plan = data.get('plan')
        
        # Validate required parameters
        if not all([domaine, sujet, plan]):
            return jsonify({'error': 'Missing required fields: domaine, sujet, plan'}), 400
        
        # Generate the content
        start_time = time.time()
        content = generate_content(domaine, sujet, plan)
        execution_time = round(time.time() - start_time, 2)
        
        # Return the content with timing information
        return jsonify({
            'success': True,
            'execution_time_seconds': execution_time,
            'content': content
        })
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating content: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to generate content: {str(e)}'}), 500

@main.route('/api/generate-files', methods=['POST'])
def api_generate_files():
    """Generate PDF and/or PPTX files from the provided content."""
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract required parameters
        sujet = data.get('sujet')
        contenu = data.get('contenu')
        format_type = data.get('format', 'pdf')  # pdf, pptx, or both
        trainer_name = data.get('trainer_name', 'AIT TALEB AYOUB')
        logo_path = data.get('logo_path', os.path.join(current_app.config['UPLOAD_FOLDER'], 'ODC_logo.jpeg'))
        
        # Validate required parameters
        if not all([sujet, contenu]):
            return jsonify({'error': 'Missing required fields: sujet, contenu'}), 400
        
        # Check if the format is valid
        if format_type not in ['pdf', 'pptx', 'both']:
            return jsonify({'error': 'Invalid format. Must be one of: pdf, pptx, both'}), 400
        
        file_paths = []
        start_time = time.time()
        
        # Generate PDF if requested
        if format_type in ['pdf', 'both']:
            pdf_filename = f"{sujet}_{int(time.time())}.pdf"
            pdf_path = os.path.join(current_app.config['OUTPUT_FOLDER'], pdf_filename)
            
            create_pdf(pdf_path, contenu, logo_path, sujet, trainer_name)
            file_paths.append({
                'type': 'pdf',
                'filename': pdf_filename,
                'path': pdf_path,
                'download_url': f"/api/download/{pdf_filename}"
            })
        
        # Generate PPTX if requested
        if format_type in ['pptx', 'both']:
            pptx_filename = f"{sujet}_{int(time.time())}.pptx"
            pptx_path = os.path.join(current_app.config['OUTPUT_FOLDER'], pptx_filename)
            
            generate_powerpoint(sujet, contenu, trainer_name, logo_path, pptx_path)
            file_paths.append({
                'type': 'pptx',
                'filename': pptx_filename,
                'path': pptx_path,
                'download_url': f"/api/download/{pptx_filename}"
            })
        
        execution_time = round(time.time() - start_time, 2)
        
        # Return information about generated files
        return jsonify({
            'success': True,
            'execution_time_seconds': execution_time,
            'files': file_paths
        })
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating files: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to generate files: {str(e)}'}), 500

@main.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a generated file."""
    return send_from_directory(
        current_app.config['OUTPUT_FOLDER'],
        filename,
        as_attachment=True
    )

@main.route('/api/generate-plan-jour', methods=['POST'])
def api_generate_plan_jour():
    """Generate a presentation plan organized by days based on provided parameters."""
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract required parameters
        domaine = data.get('domaine')
        sujet = data.get('sujet')
        description_sujet = data.get('description_sujet', '')
        niveau_apprenant = data.get('niveau_apprenant')
        nombre_jours = data.get('nombre_jours', 2)  # Default to 2 days if not specified
        
        # Validate required parameters
        if not all([domaine, sujet, niveau_apprenant]):
            return jsonify({'error': 'Missing required fields: domaine, sujet, niveau_apprenant'}), 400
        
        # Validate nombre_jours is an integer
        try:
            nombre_jours = int(nombre_jours)
            if nombre_jours < 1:
                return jsonify({'error': 'nombre_jours must be at least 1'}), 400
        except (TypeError, ValueError):
            return jsonify({'error': 'nombre_jours must be a valid integer'}), 400
        
        # Generate the daily plan
        start_time = time.time()
        plan_jour = generate_plan_jour(domaine, sujet, description_sujet, niveau_apprenant, nombre_jours)
        execution_time = round(time.time() - start_time, 2)
        
        # Return the plan with timing information
        return jsonify({
            'success': True,
            'execution_time_seconds': execution_time,
            'plan_jour': plan_jour
        })
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating daily plan: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to generate daily plan: {str(e)}'}), 500