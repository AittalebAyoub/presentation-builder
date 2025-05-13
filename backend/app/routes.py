# app/routes.py
from flask import Blueprint, jsonify, request, current_app, url_for, send_from_directory
import os
import json
import logging
import uuid
from app.services import (
    generate_plan, generate_content, create_pdf, generate_powerpoint, 
    create_quiz, create_google_form_quiz, share_form_with_user, notify_users_about_quiz
)
from app.utils.helpers import ensure_dir, save_to_json, text_to_safe_filename

# Set up logging
logger = logging.getLogger(__name__)

# Create main blueprint
main = Blueprint('main', __name__)

@main.route('/api/generate-plan', methods=['POST'])
def api_generate_plan():
    """Generate a presentation plan based on provided parameters"""
    try:
        data = request.json
        
        # Extract required parameters
        domaine = data.get('domaine')
        sujet = data.get('sujet')
        description_sujet = data.get('description_sujet', '')
        niveau_apprenant = data.get('niveau_apprenant', 'intermediaire')
        
        # Check for required parameters
        if not domaine or not sujet:
            return jsonify({'success': False, 'message': 'Missing required parameters'}), 400
        
        # Generate plan
        plan = generate_plan(domaine, sujet, description_sujet, niveau_apprenant)
        
        # Save plan to JSON file
        plan_filename = f"{text_to_safe_filename(sujet)}_plan.json"
        save_to_json(plan, plan_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'plan': plan,
            'message': 'Plan generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating plan: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating plan: {str(e)}'}), 500

@main.route('/api/generate-content', methods=['POST'])
def api_generate_content():
    """Generate content based on a presentation plan"""
    try:
        data = request.json
        
        # Extract required parameters
        domaine = data.get('domaine')
        sujet = data.get('sujet')
        plan = data.get('plan')
        
        # Check for required parameters
        if not domaine or not sujet or not plan:
            return jsonify({'success': False, 'message': 'Missing required parameters'}), 400
        
        # Generate content
        content = generate_content(domaine, sujet, plan)
        
        # Save content to JSON file
        content_filename = f"{text_to_safe_filename(sujet)}_content.json"
        save_to_json(content, content_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'content': content,
            'message': 'Content generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating content: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating content: {str(e)}'}), 500

@main.route('/api/generate-files', methods=['POST'])
def api_generate_files():
    """Generate presentation files (PDF/PPTX) from content"""
    try:
        data = request.json
        
        # Extract required parameters
        sujet = data.get('sujet')
        contenu = data.get('contenu')
        format_type = data.get('format', 'pdf')
        trainer_name = data.get('trainer_name', 'Formateur')
        
        # Check for required parameters
        if not sujet or not contenu:
            return jsonify({'success': False, 'message': 'Missing required parameters'}), 400
        
        # Create output directory if it doesn't exist
        output_dir = current_app.config['OUTPUT_FOLDER']
        ensure_dir(output_dir)
        
        # Generate files based on requested format
        files = []
        safe_filename = text_to_safe_filename(sujet)
        
        # Logo path - use default if not provided
        logo_path = os.path.join(current_app.root_path, 'static', 'img', 'ODC_logo.jpeg')
        
        if format_type in ['pdf', 'both']:
            # Generate PDF
            pdf_filename = f"{safe_filename}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            create_pdf(pdf_path, contenu, logo_path, sujet, trainer_name)
            
            # Create download URL
            pdf_url = url_for('main.download_file', filename=pdf_filename)
            files.append({
                'type': 'pdf',
                'filename': pdf_filename,
                'download_url': pdf_url
            })
        
        if format_type in ['pptx', 'both']:
            # Generate PPTX
            pptx_filename = f"{safe_filename}.pptx"
            pptx_path = os.path.join(output_dir, pptx_filename)
            generate_powerpoint(sujet, contenu, trainer_name, logo_path, pptx_path)
            
            # Create download URL
            pptx_url = url_for('main.download_file', filename=pptx_filename)
            files.append({
                'type': 'pptx',
                'filename': pptx_filename,
                'download_url': pptx_url
            })
        
        # Return response
        return jsonify({
            'success': True,
            'files': files,
            'message': 'Files generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating files: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating files: {str(e)}'}), 500

@main.route('/api/download/<filename>')
def download_file(filename):
    """Download a generated file"""
    return send_from_directory(
        current_app.config['OUTPUT_FOLDER'], 
        filename, 
        as_attachment=True
    )

# New routes for quiz functionality
@main.route('/api/generate-quiz', methods=['POST'])
def api_generate_quiz():
    """Generate quiz questions based on presentation content"""
    try:
        data = request.json
        
        # Extract required parameters
        content = data.get('content')
        level = data.get('level', current_app.config['DEFAULT_QUIZ_DIFFICULTY'])
        nbr_qst = data.get('nbr_qst', current_app.config['DEFAULT_QUIZ_QUESTIONS'])
        title = data.get('title', 'Quiz de formation')
        
        # Check for required parameters
        if not content:
            return jsonify({'success': False, 'message': 'Missing content parameter'}), 400
        
        # Validate difficulty level
        if level not in current_app.config['QUIZ_DIFFICULTY_LEVELS']:
            level = current_app.config['DEFAULT_QUIZ_DIFFICULTY']
        
        # Convert nbr_qst to int if necessary
        if isinstance(nbr_qst, str):
            try:
                nbr_qst = int(nbr_qst)
            except ValueError:
                nbr_qst = current_app.config['DEFAULT_QUIZ_QUESTIONS']
        
        # Generate quiz
        quiz_data, error = create_quiz(content, level, nbr_qst)
        
        if not quiz_data or error:
            return jsonify({
                'success': False, 
                'message': error or 'Failed to generate quiz'
            }), 500
        
        # Save quiz data
        safe_title = text_to_safe_filename(title)
        quiz_filename = f"{safe_title}_quiz_{uuid.uuid4().hex[:8]}.json"
        saved_path = save_to_json(quiz_data, quiz_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'quiz_data': quiz_data,
            'quiz_file': quiz_filename,
            'title': title,
            'message': 'Quiz generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating quiz: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating quiz: {str(e)}'}), 500

@main.route('/api/create-google-form', methods=['POST'])
def api_create_google_form():
    """Create a Google Form for the quiz"""
    try:
        data = request.json
        
        # Extract required parameters
        quiz_data = data.get('quiz_data')
        title = data.get('title', 'Quiz de formation')
        
        # Check for required parameters
        if not quiz_data:
            return jsonify({'success': False, 'message': 'Missing quiz_data parameter'}), 400
        
        # Create Google Form
        form_info = create_google_form_quiz(quiz_data, title)
        
        if not form_info:
            return jsonify({
                'success': False, 
                'message': 'Failed to create Google Form'
            }), 500
        
        # Remove credentials from response
        response_info = {
            'form_id': form_info['form_id'],
            'edit_url': form_info['edit_url'],
            'view_url': form_info['view_url'],
            'title': form_info['title']
        }
        
        # Store form info for sharing (remove credentials first)
        form_info_to_save = response_info.copy()
        form_session_id = uuid.uuid4().hex
        session_filename = f"form_session_{form_session_id}.json"
        save_to_json(form_info_to_save, session_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'form': response_info,
            'session_id': form_session_id,
            'message': 'Google Form created successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error creating Google Form: {str(e)}")
        return jsonify({'success': False, 'message': f'Error creating Google Form: {str(e)}'}), 500

@main.route('/api/share-form', methods=['POST'])
def api_share_form():
    """Share a Google Form with users"""
    try:
        data = request.json
        
        # Extract required parameters
        form_id = data.get('form_id')
        emails = data.get('emails', [])
        trainer_emails = data.get('trainer_emails', [])
        session_id = data.get('session_id')
        
        # Check for required parameters
        if not form_id or (not emails and not trainer_emails):
            return jsonify({
                'success': False, 
                'message': 'Missing required parameters (form_id, emails)'
            }), 400
        
        # Get form info from session if available
        form_info = None
        if session_id:
            session_filename = f"form_session_{session_id}.json"
            form_info_path = os.path.join(current_app.config['OUTPUT_FOLDER'], session_filename)
            
            if os.path.exists(form_info_path):
                with open(form_info_path, 'r') as f:
                    form_info = json.load(f)
        
        if not form_info:
            form_info = {
                'form_id': form_id,
                'title': data.get('title', 'Quiz de formation'),
                'edit_url': data.get('edit_url'),
                'view_url': data.get('view_url')
            }
        
        # Prepare users list for notification
        users_list = []
        
        # Share with trainers (who can edit)
        for email in trainer_emails:
            # Share the form
            shared = share_form_with_user(form_id, email)
            
            # Add to notification list
            if shared:
                users_list.append({
                    'email': email,
                    'is_trainer': True
                })
        
        # Add regular users to notification list
        for email in emails:
            users_list.append({
                'email': email,
                'is_trainer': False
            })
        
        # Send email notifications
        if users_list:
            notification_results = notify_users_about_quiz(form_info, users_list)
        else:
            notification_results = {'successful': [], 'failed': []}
        
        # Return response
        return jsonify({
            'success': True,
            'form_id': form_id,
            'shared_with': notification_results,
            'message': 'Form shared successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error sharing form: {str(e)}")
        return jsonify({'success': False, 'message': f'Error sharing form: {str(e)}'}), 500

@main.route('/api/quiz-workflow', methods=['POST'])
def api_quiz_workflow():
    """Complete quiz workflow: generate, create form, and share"""
    try:
        data = request.json
        
        # Extract required parameters
        content = data.get('content')
        title = data.get('title', 'Quiz de formation')
        level = data.get('level', current_app.config['DEFAULT_QUIZ_DIFFICULTY'])
        nbr_qst = data.get('nbr_qst', current_app.config['DEFAULT_QUIZ_QUESTIONS'])
        emails = data.get('emails', [])
        trainer_emails = data.get('trainer_emails', [])
        
        # Check for required parameters
        if not content:
            return jsonify({'success': False, 'message': 'Missing content parameter'}), 400
        
        # Step 1: Generate quiz
        quiz_data, error = create_quiz(content, level, nbr_qst)
        
        if not quiz_data or error:
            return jsonify({
                'success': False, 
                'message': error or 'Failed to generate quiz'
            }), 500
        
        # Step 2: Create Google Form
        form_info = create_google_form_quiz(quiz_data, title)
        
        if not form_info:
            return jsonify({
                'success': False, 
                'message': 'Failed to create Google Form'
            }), 500
        
        # Step 3: Share with users
        users_list = []
        
        # Share with trainers (who can edit)
        for email in trainer_emails:
            # Share using the credentials from form creation
            shared = share_form_with_user(
                form_info['form_id'], 
                email, 
                form_info.get('credentials')
            )
            
            # Add to notification list
            if shared:
                users_list.append({
                    'email': email,
                    'is_trainer': True
                })
        
        # Add regular users to notification list
        for email in emails:
            users_list.append({
                'email': email,
                'is_trainer': False
            })
        
        # Send email notifications
        if users_list:
            notification_results = notify_users_about_quiz(form_info, users_list)
        else:
            notification_results = {'successful': [], 'failed': []}
        
        # Prepare response
        response_info = {
            'form_id': form_info['form_id'],
            'edit_url': form_info['edit_url'],
            'view_url': form_info['view_url'],
            'title': form_info['title']
        }
        
        # Return response with all information
        return jsonify({
            'success': True,
            'quiz_data': quiz_data,
            'form': response_info,
            'shared_with': notification_results,
            'message': 'Quiz workflow completed successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error in quiz workflow: {str(e)}")
        return jsonify({'success': False, 'message': f'Error in quiz workflow: {str(e)}'}), 500