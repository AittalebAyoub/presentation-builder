# app/routes.py
from flask import Blueprint, jsonify, request, current_app, url_for, send_from_directory
import os
import json
import logging
import uuid
from app.services import (
    generate_plan, generate_content, create_pdf, generate_powerpoint, 
    create_quiz, create_google_form_quiz, share_form_with_user, notify_users_about_quiz,
    # Add these new imports for multi-quiz functionality
    generate_quiz_for_days, generate_quiz_for_sections, create_multiple_forms
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

# New routes for multi-quiz functionality (daily and section-based quizzes)

@main.route('/api/generate-daily-quizzes', methods=['POST'])
def api_generate_daily_quizzes():
    """Generate quizzes for each day of content"""
    try:
        data = request.json
        
        # Extract required parameters
        daily_content = data.get('daily_content')
        level = data.get('level', current_app.config['DEFAULT_QUIZ_DIFFICULTY'])
        nbr_qst_per_day = data.get('nbr_qst_per_day', current_app.config['DEFAULT_QUIZ_QUESTIONS'])
        title_template = data.get('title_template', 'Formation')
        
        # Check for required parameters
        if not daily_content:
            return jsonify({'success': False, 'message': 'Missing daily_content parameter'}), 400
        
        # Validate difficulty level
        if level not in current_app.config['QUIZ_DIFFICULTY_LEVELS']:
            level = current_app.config['DEFAULT_QUIZ_DIFFICULTY']
        
        # Convert nbr_qst_per_day to int if necessary
        if isinstance(nbr_qst_per_day, str):
            try:
                nbr_qst_per_day = int(nbr_qst_per_day)
            except ValueError:
                nbr_qst_per_day = current_app.config['DEFAULT_QUIZ_QUESTIONS']
        
        # Generate quizzes for each day
        quizzes, errors = generate_quiz_for_days(daily_content, level, nbr_qst_per_day)
        
        # Check for complete failure
        if not quizzes or all(q is None for q in quizzes):
            return jsonify({
                'success': False,
                'message': 'Failed to generate any quizzes',
                'errors': errors
            }), 500
        
        # Create a session ID for storing the generated quizzes
        session_id = uuid.uuid4().hex
        quiz_filename = f"daily_quizzes_{session_id}.json"
        
        # Save quiz data (only the valid ones)
        quiz_data_to_save = [q for q in quizzes if q is not None]
        if quiz_data_to_save:
            save_to_json(quiz_data_to_save, quiz_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'quizzes': quizzes,
            'session_id': session_id,
            'total_days': len(daily_content),
            'successful_days': sum(1 for q in quizzes if q is not None),
            'errors': errors,
            'message': 'Daily quizzes generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating daily quizzes: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating daily quizzes: {str(e)}'}), 500

@main.route('/api/generate-section-quizzes', methods=['POST'])
def api_generate_section_quizzes():
    """Generate quizzes for each section of content"""
    try:
        data = request.json
        
        # Extract required parameters
        section_content = data.get('section_content')
        level = data.get('level', current_app.config['DEFAULT_QUIZ_DIFFICULTY'])
        nbr_qst_per_section = data.get('nbr_qst_per_section', current_app.config['DEFAULT_QUIZ_QUESTIONS'])
        title_template = data.get('title_template', 'Formation')
        
        # Check for required parameters
        if not section_content:
            return jsonify({'success': False, 'message': 'Missing section_content parameter'}), 400
        
        # Validate difficulty level
        if level not in current_app.config['QUIZ_DIFFICULTY_LEVELS']:
            level = current_app.config['DEFAULT_QUIZ_DIFFICULTY']
        
        # Convert nbr_qst_per_section to int if necessary
        if isinstance(nbr_qst_per_section, str):
            try:
                nbr_qst_per_section = int(nbr_qst_per_section)
            except ValueError:
                nbr_qst_per_section = current_app.config['DEFAULT_QUIZ_QUESTIONS']
        
        # Generate quizzes for each section
        quizzes, errors = generate_quiz_for_sections(section_content, level, nbr_qst_per_section)
        
        # Check for complete failure
        if not quizzes or all(q is None for q in quizzes):
            return jsonify({
                'success': False,
                'message': 'Failed to generate any quizzes',
                'errors': errors
            }), 500
        
        # Create a session ID for storing the generated quizzes
        session_id = uuid.uuid4().hex
        quiz_filename = f"section_quizzes_{session_id}.json"
        
        # Save quiz data (only the valid ones)
        quiz_data_to_save = [q for q in quizzes if q is not None]
        if quiz_data_to_save:
            save_to_json(quiz_data_to_save, quiz_filename)
        
        # Return response
        return jsonify({
            'success': True,
            'quizzes': quizzes,
            'session_id': session_id,
            'total_sections': len(section_content),
            'successful_sections': sum(1 for q in quizzes if q is not None),
            'errors': errors,
            'message': 'Section quizzes generated successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error generating section quizzes: {str(e)}")
        return jsonify({'success': False, 'message': f'Error generating section quizzes: {str(e)}'}), 500

@main.route('/api/create-multiple-forms', methods=['POST'])
def api_create_multiple_forms():
    """Create multiple Google Forms from quiz data"""
    try:
        data = request.json
        
        # Extract required parameters
        quiz_data_list = data.get('quiz_data_list')
        title_template = data.get('title_template', 'Formation')
        type = data.get('type', 'day')  # 'day' or 'section'
        
        # Check for required parameters
        if not quiz_data_list:
            return jsonify({'success': False, 'message': 'Missing quiz_data_list parameter'}), 400
        
        # Validate type
        if type not in ['day', 'section']:
            return jsonify({'success': False, 'message': 'Type must be "day" or "section"'}), 400
        
        # Create forms
        forms, errors = create_multiple_forms(quiz_data_list, title_template, type)
        
        # Check for complete failure
        if not forms or all(f is None for f in forms):
            return jsonify({
                'success': False,
                'message': 'Failed to create any forms',
                'errors': errors
            }), 500
        
        # Process forms to remove credentials from the response
        response_forms = []
        for form in forms:
            if form:
                response_forms.append({
                    'form_id': form.get('form_id'),
                    'edit_url': form.get('edit_url'),
                    'view_url': form.get('view_url'),
                    'title': form.get('title')
                })
            else:
                response_forms.append(None)
        
        # Return response
        return jsonify({
            'success': True,
            'forms': response_forms,
            'total_items': len(quiz_data_list),
            'successful_forms': sum(1 for f in forms if f is not None),
            'errors': errors,
            'message': f'Multiple forms created successfully'
        })
        
    except Exception as e:
        logger.exception(f"Error creating multiple forms: {str(e)}")
        return jsonify({'success': False, 'message': f'Error creating multiple forms: {str(e)}'}), 500

@main.route('/api/multi-quiz-workflow', methods=['POST'])
def api_multi_quiz_workflow():
    """Complete workflow for multiple quizzes: generate, create forms, and share"""
    try:
        data = request.json
        
        # Extract required parameters
        content = data.get('content')
        type = data.get('type', 'day')  # 'day' or 'section'
        level = data.get('level', current_app.config['DEFAULT_QUIZ_DIFFICULTY'])
        nbr_qst_per_item = data.get('nbr_qst_per_item', current_app.config['DEFAULT_QUIZ_QUESTIONS'])
        title_template = data.get('title_template', 'Formation')
        emails = data.get('emails', [])
        trainer_emails = data.get('trainer_emails', [])
        share_forms = data.get('share_forms', False)
        
        # Check for required parameters
        if not content:
            return jsonify({'success': False, 'message': 'Missing content parameter'}), 400
        
        # Validate type
        if type not in ['day', 'section']:
            return jsonify({'success': False, 'message': 'Type must be "day" or "section"'}), 400
        
        # Step 1: Generate quizzes
        if type == 'day':
            quizzes, quiz_errors = generate_quiz_for_days(content, level, nbr_qst_per_item)
        else:
            quizzes, quiz_errors = generate_quiz_for_sections(content, level, nbr_qst_per_item)
        
        # Check for complete quiz generation failure
        if not quizzes or all(q is None for q in quizzes):
            return jsonify({
                'success': False,
                'message': 'Failed to generate any quizzes',
                'errors': quiz_errors
            }), 500
        
        # Step 2: Create forms
        forms, form_errors = create_multiple_forms(quizzes, title_template, type)
        
        # Process forms for response
        response_forms = []
        valid_forms = []
        
        for form in forms:
            if form:
                form_data = {
                    'form_id': form.get('form_id'),
                    'edit_url': form.get('edit_url'),
                    'view_url': form.get('view_url'),
                    'title': form.get('title')
                }
                response_forms.append(form_data)
                valid_forms.append(form)
            else:
                response_forms.append(None)
        
        # Step 3: Share forms if requested
        share_results = []
        if share_forms and (emails or trainer_emails) and valid_forms:
            for form in valid_forms:
                # Create users list for notifications
                users_list = []
                
                # Share with trainers (who can edit)
                for email in trainer_emails:
                    shared = share_form_with_user(form.get('form_id'), email, form.get('credentials'))
                    if shared:
                        users_list.append({
                            'email': email,
                            'is_trainer': True
                        })
                
                # Add regular users
                for email in emails:
                    users_list.append({
                        'email': email,
                        'is_trainer': False
                    })
                
                # Send notifications
                if users_list:
                    notification_result = notify_users_about_quiz(form, users_list)
                    share_results.append({
                        'form_id': form.get('form_id'),
                        'title': form.get('title'),
                        'results': notification_result
                    })
        
        # Return response
        response = {
            'success': True,
            'quizzes': quizzes,
            'forms': response_forms,
            'total_items': len(content),
            'successful_quizzes': sum(1 for q in quizzes if q is not None),
            'successful_forms': sum(1 for f in forms if f is not None),
            'quiz_errors': quiz_errors,
            'form_errors': form_errors,
            'message': f'Multiple quiz workflow completed successfully'
        }
        
        if share_forms and share_results:
            response['share_results'] = share_results
        
        return jsonify(response)
        
    except Exception as e:
        logger.exception(f"Error in multi-quiz workflow: {str(e)}")
        return jsonify({'success': False, 'message': f'Error in multi-quiz workflow: {str(e)}'}), 500