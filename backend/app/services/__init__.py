# Import the service functions to make them available directly from the services package
from app.services.plan_generator import generate_plan
from app.services.content_generator import generate_content
from app.services.pdf_generator import create_pdf
from app.services.pptx_generator import generate_powerpoint
from app.services.quiz_generator import create_quiz
from app.services.google_forms_service import create_google_form_quiz, share_form_with_user
from app.services.email_service import send_email, send_quiz_notification, notify_users_about_quiz