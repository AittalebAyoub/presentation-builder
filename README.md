# Presentation Builder

A web application that generates professional presentations from user inputs using AI.

**Live Demo:** [https://presentation-builder-1.onrender.com](https://presentation-builder-1.onrender.com)

![Presentation Builder Screenshot](https://via.placeholder.com/800x450)

## Overview

Presentation Builder is a full-stack web application that allows users to quickly create professional presentations by leveraging AI technology. The application takes user inputs such as the topic, audience level, and description, then automatically generates a structured presentation plan, detailed content, and exports it to PDF or PowerPoint formats.

## Features

- **3-Step Presentation Creation Process**:
  - Step 1: Set parameters (topic, audience level, format, etc.)
  - Step 2: Customize the presentation plan
  - Step 3: Generate presentation files (PDF/PowerPoint)
- **AI-Powered Content Generation**:
  - Automatically generates structured presentation plans
  - Creates detailed content for each section
  - Supports multiple output formats (PDF, PPTX)
- **Interactive Plan Editor**:
  - Add/edit/remove sections and subsections
  - Reorder sections with drag-and-drop
- **Modern, Responsive UI**:
  - Clean, intuitive interface
  - Progress tracking
  - Loading indicators

## Technology Stack

### Frontend
- React.js
- CSS3 with custom styling
- Font Awesome for icons
- Responsive design

### Backend
- Flask (Python)
- OpenAI API for content generation
- ReportLab for PDF generation
- python-pptx for PowerPoint generation

## Project Structure

The project follows a client-server architecture:

### Frontend
- React components for UI
- State management with React hooks
- API services for backend communication

### Backend
- Flask application with RESTful endpoints
- Services for plan generation, content creation, and file export
- Modular architecture with separate services for each functionality

## Installation and Setup

### Prerequisites
- Node.js and npm
- Python 3.8+
- pip

### Backend Setup
1. Clone the repository
   ```bash
   git clone <repository-url>
   cd presentation-builder
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export OPENAI_API_KEY=your-api-key  # Required for AI content generation
   ```

5. Run the Flask application
   ```bash
   python run.py
   ```

### Frontend Setup
1. Navigate to the frontend directory
   ```bash
   cd frontend
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Start the development server
   ```bash
   npm start
   ```

4. The application should now be running at `http://localhost:3000`

## API Endpoints

The backend exposes the following API endpoints:

- `POST /api/generate-plan` - Generate a presentation plan
- `POST /api/generate-content` - Generate detailed content for the plan
- `POST /api/generate-files` - Create PDF/PPTX files from content

## Deployment

The application is deployed on Render:
- Frontend: Static site hosting
- Backend: Web service

## Future Enhancements

- User authentication and saved presentations
- More customization options for templates and themes
- Support for more output formats
- Advanced editing features for content
- Image generation for slides

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Orange Digital Center for the UI design inspiration
- OpenAI for the content generation capabilities