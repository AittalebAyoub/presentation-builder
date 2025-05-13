# app/services/email_service.py
import base64
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
from app.utils.google_auth_utils import build_gmail_service

logger = logging.getLogger(__name__)

def create_message(sender, to, subject, message_text, html_content=None):
    """
    Create an email message
    
    Args:
        sender: Email sender
        to: Email recipient
        subject: Email subject
        message_text: Plain text content
        html_content: Optional HTML content
        
    Returns:
        dict: Email message in the format required by Gmail API
    """
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    # Attach plain text part
    part1 = MIMEText(message_text, 'plain')
    message.attach(part1)
    
    # Attach HTML part if provided
    if html_content:
        part2 = MIMEText(html_content, 'html')
        message.attach(part2)
    
    # Encode message for Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(to, subject, body_text, html_content=None):
    """
    Send an email using Gmail API
    
    Args:
        to: Email recipient
        subject: Email subject
        body_text: Plain text email body
        html_content: Optional HTML email body
        
    Returns:
        dict: Information about the sent message or None if error
    """
    try:
        gmail_service = build_gmail_service()
        
        if not gmail_service:
            logger.error("Failed to create Gmail service")
            return None
        
        sender = current_app.config.get('EMAIL_SENDER', 'noreply@example.com')
        
        message = create_message(sender, to, subject, body_text, html_content)
        
        sent_message = gmail_service.users().messages().send(
            userId="me", 
            body=message
        ).execute()
        
        logger.info(f"Email sent to {to}, message ID: {sent_message['id']}")
        return sent_message
    
    except Exception as e:
        logger.error(f"Error sending email to {to}: {e}")
        return None

def send_quiz_notification(recipient_email, quiz_title, view_url, edit_url=None):
    """
    Send a notification email about a newly created quiz
    
    Args:
        recipient_email: Email of the recipient
        quiz_title: Title of the quiz
        view_url: URL to view the quiz
        edit_url: Optional URL to edit the quiz (for trainers)
        
    Returns:
        dict: Information about the sent message or None if error
    """
    subject = f"Nouveau Quiz: {quiz_title}"
    
    is_trainer = edit_url is not None
    
    # Plain text email
    body_text = f"""
Bonjour,

Un nouveau quiz intitulé "{quiz_title}" a été créé.

{'Vous pouvez le modifier ici: ' + edit_url if is_trainer else ''}
Vous pouvez y accéder ici: {view_url}

Merci,
L'équipe de formation
    """
    
    # HTML email
    html_content = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .button {{ display: inline-block; background-color: #FF7900; color: white; 
                  padding: 10px 20px; text-decoration: none; border-radius: 5px; 
                  margin: 10px 0; }}
        .footer {{ font-size: 12px; color: #777; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Nouveau Quiz Disponible</h2>
        <p>Bonjour,</p>
        <p>Un nouveau quiz intitulé <strong>"{quiz_title}"</strong> a été créé.</p>
        
        {f'<p>En tant que formateur, vous pouvez modifier ce quiz :</p><p><a href="{edit_url}" class="button">Modifier le Quiz</a></p>' if is_trainer else ''}
        
        <p>Pour accéder au quiz :</p>
        <p><a href="{view_url}" class="button">Voir le Quiz</a></p>
        
        <div class="footer">
            <p>Merci,<br>L'équipe de formation</p>
        </div>
    </div>
</body>
</html>
    """
    
    return send_email(recipient_email, subject, body_text, html_content)

def notify_users_about_quiz(form_info, users_list):
    """
    Notify multiple users about a quiz
    
    Args:
        form_info: Information about the form, including URLs and title
        users_list: List of user emails or dicts with email and is_trainer flag
        
    Returns:
        dict: Information about which notifications were sent
    """
    results = {'successful': [], 'failed': []}
    
    for user in users_list:
        # Handle both simple email strings and dict objects
        if isinstance(user, dict):
            email = user.get('email')
            is_trainer = user.get('is_trainer', False)
        else:
            email = user
            is_trainer = False
        
        if not email:
            continue
        
        # For trainers, include edit URL, for regular users only include view URL
        edit_url = form_info['edit_url'] if is_trainer else None
        
        # Send the email
        sent = send_quiz_notification(
            email, 
            form_info['title'], 
            form_info['view_url'], 
            edit_url
        )
        
        if sent:
            results['successful'].append(email)
        else:
            results['failed'].append(email)
    
    return results