# app/utils/google_auth_utils.py - Updated version
import os
import pickle
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flask import current_app
import logging

# Setup logging
logger = logging.getLogger(__name__)

def get_service_account_credentials(scopes):
    """
    Get credentials from service account JSON file
    
    Args:
        scopes: List of API scopes required
        
    Returns:
        Credentials object or None if an error occurred
    """
    try:
        # Import here to avoid circular imports
        from flask import current_app
        
        service_account_file = current_app.config['GOOGLE_SERVICE_ACCOUNT_FILE']
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes)
        return credentials
    except Exception as e:
        logger.error(f"Error getting service account credentials: {e}")
        return None

def get_gmail_credentials():
    """
    Get user credentials for Gmail API using OAuth 2.0 flow
    
    Returns:
        Credentials object or None if an error occurred
    """
    try:
        # Import here to avoid circular imports
        from flask import current_app
        
        scopes = ['https://www.googleapis.com/auth/gmail.send']
        
        # Get paths from app config
        instance_path = current_app.instance_path
        token_path = os.path.join(instance_path, 'gmail_token.pickle')
        credentials_path = current_app.config['GMAIL_CREDENTIALS_FILE']
        
        # Ensure instance directory exists
        os.makedirs(instance_path, exist_ok=True)
        
        creds = None
        # Check if token file exists
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials don't exist or are invalid, refresh or obtain new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0, open_browser=False)
                
                # Save the credentials for the next run
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
        
        return creds
    except Exception as e:
        logger.error(f"Error getting Gmail credentials: {e}")
        return None

def build_forms_service():
    """
    Build and return a Google Forms API service object
    
    Returns:
        Service object for Forms API or None if an error occurred
    """
    try:
        scopes = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/drive']
        credentials = get_service_account_credentials(scopes)
        
        if not credentials:
            logger.error("Failed to get credentials for Forms service")
            return None
        
        return build('forms', 'v1', credentials=credentials)
    except Exception as e:
        logger.error(f"Error building Forms service: {e}")
        return None

def build_drive_service(credentials=None):
    """
    Build and return a Google Drive API service object
    
    Args:
        credentials: Optional credentials to use instead of getting new ones
        
    Returns:
        Service object for Drive API or None if an error occurred
    """
    try:
        if not credentials:
            scopes = ['https://www.googleapis.com/auth/drive']
            credentials = get_service_account_credentials(scopes)
        
        if not credentials:
            logger.error("Failed to get credentials for Drive service")
            return None
        
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        logger.error(f"Error building Drive service: {e}")
        return None

def build_gmail_service():
    """
    Build and return a Gmail API service object
    
    Returns:
        Service object for Gmail API or None if an error occurred
    """
    try:
        credentials = get_gmail_credentials()
        
        if not credentials:
            logger.error("Failed to get credentials for Gmail service")
            return None
        
        return build('gmail', 'v1', credentials=credentials)
    except Exception as e:
        logger.error(f"Error building Gmail service: {e}")
        return None