# app/services/google_forms_service.py
import logging
from app.utils.google_auth_utils import build_forms_service, build_drive_service, get_service_account_credentials

logger = logging.getLogger(__name__)

def create_google_form_quiz(quiz_data, title):
    """
    Create a Google Form quiz from quiz data
    
    Args:
        quiz_data: List of dictionaries containing questions/answers
        title: Title of the form
        
    Returns:
        dict: Information about the created form including URLs or None if error
    """
    # Build the Forms service
    forms_service = build_forms_service()
    
    if not forms_service:
        logger.error("Failed to create Forms service")
        return None
    
    # Create a new form
    form = {
        'info': {
            'title': title,
        }
    }
    
    try:
        # Create form
        created_form = forms_service.forms().create(body=form).execute()
        form_id = created_form['formId']
        
        # Enable quiz mode
        quiz_settings = {
            'requests': [{
                'updateSettings': {
                    'settings': {
                        'quizSettings': {
                            'isQuiz': True
                        }
                    },
                    'updateMask': 'quizSettings.isQuiz'
                }
            }]
        }
        forms_service.forms().batchUpdate(formId=form_id, body=quiz_settings).execute()
        
        # Prepare requests to add questions
        requests = []
        
        for index, question_data in enumerate(quiz_data):
            # Extract question information
            question_text = question_data.get('question', '')
            choices = []
            
            # Determine if it's a single or multiple choice question
            correct_answer_keys = question_data.get('reponse', [])
            question_type = 'RADIO' if len(correct_answer_keys) == 1 else 'CHECKBOX'
            
            # Collect all possible choices
            choice_keys = [key for key in question_data.keys() if key.startswith('choix_')]
            for choice_key in sorted(choice_keys):
                choice_value = question_data.get(choice_key, '')
                choices.append({'value': choice_value})
            
            # Create request to add the question
            request = {
                'createItem': {
                    'item': {
                        'title': question_text,
                        'questionItem': {
                            'question': {
                                'required': True,
                                'choiceQuestion': {
                                    'type': question_type,
                                    'options': choices,
                                    'shuffle': True
                                }
                            }
                        }
                    },
                    'location': {'index': index}
                }
            }
            
            requests.append(request)
        
        # Send requests to add questions
        update = {'requests': requests}
        forms_service.forms().batchUpdate(formId=form_id, body=update).execute()
        
        # Add correct answers (only for service accounts with full access)
        try:
            answer_requests = []
            
            for index, question_data in enumerate(quiz_data):
                correct_answer_keys = question_data.get('reponse', [])
                
                if not correct_answer_keys:
                    continue
                
                # Get all items to find the item ID for this question
                form_get = forms_service.forms().get(formId=form_id).execute()
                items = form_get.get('items', [])
                
                if index < len(items):
                    item_id = items[index]['itemId']
                    
                    # Get indices of correct answers
                    correct_indices = []
                    for answer_key in correct_answer_keys:
                        if answer_key.startswith('choix_'):
                            # Extract index from "choix_N" (e.g., "choix_1" -> 0)
                            choice_index = int(answer_key.split('_')[1]) - 1
                            correct_indices.append(choice_index)
                    
                    # Add answer key
                    answer_request = {
                        'createItemResponse': {
                            'questionId': item_id,
                            'correctAnswers': {
                                'answers': [{'value': str(i)} for i in correct_indices]
                            }
                        }
                    }
                    
                    answer_requests.append(answer_request)
            
            if answer_requests:
                forms_service.forms().batchUpdate(
                    formId=form_id, 
                    body={'requests': answer_requests}
                ).execute()
                
        except Exception as e:
            logger.warning(f"Failed to set correct answers: {e}")
        
        # Build URLs
        edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
        view_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
        
        # Store credentials for sharing
        scopes = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/drive']
        credentials = get_service_account_credentials(scopes)
        
        form_info = {
            'form_id': form_id,
            'edit_url': edit_url,
            'view_url': view_url,
            'title': title,
            'credentials': credentials
        }
        
        logger.info(f"Successfully created Google Form: {title}")
        return form_info
    
    except Exception as e:
        logger.error(f"Error creating Google Form: {e}")
        return None

def share_form_with_user(form_id, email, credentials=None):
    """
    Share a Google Form with a specific user
    
    Args:
        form_id: ID of the form to share
        email: Email address to share with
        credentials: Optional credentials to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        drive_service = build_drive_service(credentials)
        
        if not drive_service:
            logger.error("Failed to create Drive service for sharing")
            return False
        
        permission = {
            'type': 'user',
            'role': 'writer',  # or 'owner' to transfer ownership
            'emailAddress': email
        }
        
        drive_service.permissions().create(
            fileId=form_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()
        
        logger.info(f"Form shared with {email}")
        return True
    
    except Exception as e:
        logger.error(f"Error sharing form with {email}: {e}")
        return False