# app/services/multi_quiz_generator.py - Updated version
import logging
from concurrent.futures import ThreadPoolExecutor
from flask import current_app
from app.services.quiz_generator import create_quiz
from app.services.google_forms_service import create_google_form_quiz

logger = logging.getLogger(__name__)

def generate_quiz_for_days(daily_content, level="intermediaire", nbr_qst_per_day=3):
    """
    Generate quizzes for each day's content
    
    Args:
        daily_content: List of content for each day
        level: Difficulty level (debutant, intermediaire, avance)
        nbr_qst_per_day: Number of questions per day
        
    Returns:
        list: List of generated quiz data for each day
        list: List of days with errors
    """
    if not daily_content or not isinstance(daily_content, list):
        return [], ["Invalid daily content format"]
    
    quiz_day = []
    error_days = []
    
    for i, content in enumerate(daily_content):
        try:
            day_number = i + 1
            logger.info(f"Generating quiz for day {day_number}")
            
            # Pass the application context correctly
            quiz_data, error = create_quiz(content, level, nbr_qst_per_day)
            
            if error or not quiz_data:
                error_days.append(f"Day {day_number}: {error}")
                # Add empty quiz data as placeholder
                quiz_day.append(None)
            else:
                quiz_day.append(quiz_data)
                
        except Exception as e:
            logger.error(f"Error generating quiz for day {i+1}: {str(e)}")
            error_days.append(f"Day {i+1}: {str(e)}")
            quiz_day.append(None)
    
    return quiz_day, error_days

def generate_quiz_for_sections(section_content, level="intermediaire", nbr_qst_per_section=3):
    """
    Generate quizzes for each section's content
    
    Args:
        section_content: List of content for each section
        level: Difficulty level (debutant, intermediaire, avance)
        nbr_qst_per_section: Number of questions per section
        
    Returns:
        list: List of generated quiz data for each section
        list: List of sections with errors
    """
    if not section_content or not isinstance(section_content, list):
        return [], ["Invalid section content format"]
    
    quiz_section = []
    error_sections = []
    
    for i, content in enumerate(section_content):
        try:
            section_number = i + 1
            logger.info(f"Generating quiz for section {section_number}")
            
            # Pass the application context correctly
            quiz_data, error = create_quiz(content, level, nbr_qst_per_section)
            
            if error or not quiz_data:
                error_sections.append(f"Section {section_number}: {error}")
                # Add empty quiz data as placeholder
                quiz_section.append(None)
            else:
                quiz_section.append(quiz_data)
                
        except Exception as e:
            logger.error(f"Error generating quiz for section {i+1}: {str(e)}")
            error_sections.append(f"Section {i+1}: {str(e)}")
            quiz_section.append(None)
    
    return quiz_section, error_sections

def create_multiple_forms(quiz_data_list, title_template, type="day"):
    """
    Create multiple Google Forms from a list of quiz data
    
    Args:
        quiz_data_list: List of quiz data for each day/section
        title_template: Template for form titles
        type: 'day' or 'section'
        
    Returns:
        list: List of form information dictionaries
        list: List of errors
    """
    if not quiz_data_list or not isinstance(quiz_data_list, list):
        return [], ["Invalid quiz data list format"]
    
    forms = []
    errors = []
    
    # Use standard for loop instead of ThreadPoolExecutor to avoid application context issues
    for i, quiz_data in enumerate(quiz_data_list):
        if not quiz_data:
            forms.append(None)
            errors.append(f"{type.capitalize()} {i+1}: No quiz data available")
            continue
        
        try:
            item_number = i + 1
            title = f"{title_template}: Quiz du {type} {item_number}"
            
            # Create the form
            form_info = create_google_form_quiz(quiz_data, title)
            
            if not form_info:
                forms.append(None)
                errors.append(f"{type.capitalize()} {item_number}: Failed to create form")
            else:
                forms.append(form_info)
                
        except Exception as e:
            logger.error(f"Error creating form for {type} {i+1}: {str(e)}")
            forms.append(None)
            errors.append(f"{type.capitalize()} {i+1}: {str(e)}")
    
    return forms, errors