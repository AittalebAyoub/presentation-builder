from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Image, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Preformatted
import os

def format_code_block(code_text):
    """
    Format code blocks for PDF display
    
    Args:
        code_text: List of code lines
        
    Returns:
        Formatted table containing code with proper styling
    """
    # Join code lines with line breaks
    code_text = "\n".join(code_text)
    
    # Use Preformatted to preserve spaces
    formatted_code = Preformatted(code_text, getSampleStyleSheet()["Code"])
    
    code_table = Table([[formatted_code]])
    
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f3f3f3")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#222222")),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    return code_table

def format_table(data):
    """
    Format tables for PDF display
    
    Args:
        data: 2D list representing table data
        
    Returns:
        Formatted table with proper styling
    """
    # Wrap each cell value in a Paragraph
    wrapped_data = [[Paragraph(str(cell), getSampleStyleSheet()['Normal']) for cell in row] for row in data]
    table = Table(wrapped_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0097b2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#f3f3f3")),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffffff")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    return table

def create_pdf(output_filename, sections, logo_path, formation_title, trainer_name):
    """
    Create a PDF presentation from the generated content
    
    Args:
        output_filename: Path to save the PDF file
        sections: Content sections to include
        logo_path: Path to the logo image
        formation_title: Title of the presentation
        trainer_name: Name of the presenter
    """
    page_width, page_height = 600, 350
    
    doc = SimpleDocTemplate(output_filename, pagesize=(page_width, page_height),
                            leftMargin=15, rightMargin=15, topMargin=10, bottomMargin=15)
    
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    
    # Styles customization
    formation_style = ParagraphStyle(
        "FormationTitle",
        parent=styles["Title"],
        fontSize=45,
        textColor=colors.HexColor("#ff7900"),
        spaceAfter=15,
        spaceBefore=45,
        alignment=TA_LEFT,
    )
    
    trainer_style = ParagraphStyle(
        "TrainerName",
        parent=styles["BodyText"],
        fontSize=25,
        spaceAfter=45,
        spaceBefore=45,
        alignment=TA_CENTER,
        leftIndent=45,
    )
    
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=14,
        alignment=TA_LEFT,
        spaceAfter=5,
        spaceBefore=5,
        textColor=colors.HexColor("#ff7900")
    )
    
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=17,
        spaceBefore=3,
        spaceAfter=3,
        rightIndent=15,
        fontName="Courier",
    )
    
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["BodyText"],
        fontSize=12,
        spaceAfter=2,
        textColor=colors.HexColor("#000"),
        leftIndent=15,
        fontName="Helvetica-Bold"
    )
    
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=20,
        spaceAfter=3,
        leftIndent=30,
        rightIndent=15,
        alignment=TA_JUSTIFY
    )
    
    elements = []
    
    # Function to add the orange bar
    def add_orange_bar(c, width, height):
        orange = colors.HexColor("#ff7900")
        c.setFillColor(orange)
        c.rect(-12, 0, 20, height, fill=True, stroke=False)
    
    # Check if logo exists, use placeholder if not
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'default_logo.png')
        # If default logo doesn't exist either, create a blank image
        if not os.path.exists(logo_path):
            from PIL import Image as PILImage
            from PIL import ImageDraw
            img = PILImage.new('RGB', (150, 50), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((10, 20), "Logo", fill=(0, 0, 0))
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'default_logo.png')
            img.save(logo_path)
    
    # Add first page (Formation)
    img = Image(logo_path, width=120, height=30)
    img.hAlign = 'RIGHT'
    
    elements.append(img)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Formation", formation_style))
    elements.append(Paragraph(formation_title, trainer_style))
    elements.append(PageBreak())
    
    # Add second page (Presented by)
    elements.append(img)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Présenté par", formation_style))
    elements.append(Paragraph(trainer_name, trainer_style))
    elements.append(PageBreak())
    
    # Add content
    for sections_group in sections:
        for section in sections_group:
            section_title = section.get("title", "Sans titre")
            elements.append(Paragraph(f"<b>{section_title}</b>", title_style))
            elements.append(Spacer(1, 10))
            
            # Handle subsections
            for subsection in section.get("subsections", []):
                subsection_title = subsection.get("title", "Sous-section")
                elements.append(Paragraph(f"{subsection_title}", subtitle_style))
                elements.append(Spacer(1, 5))
                
                # Main content
                content = subsection.get("content", "")
                elements.append(Paragraph(content, body_style))
                elements.append(Spacer(1, 10))
                
                # Bullet points
                if "bullets" in subsection:
                    bullet_points = ListFlowable(
                        [ListItem(Paragraph(point, bullet_style)) for point in subsection["bullets"]],
                        bulletType="bullet",
                        leftIndent=25,
                        spaceBefore=5,
                        spaceAfter=5
                    )
                    elements.append(bullet_points)
                    elements.append(Spacer(1, 10))
                
                # Code blocks
                if "code" in subsection :
                    try : 
                        elements.append(format_code_block(subsection["code"]))
                        elements.append(Spacer(1, 10))
                
                    except Exception as e :
                        print(f'Code : {e}')
                
                # Tables
                if "table" in subsection :
                    try : 
                      table_data = subsection["table"]
                      elements.append(format_table(table_data))
                      elements.append(Spacer(1, 10))
                
                    except Exception as e :
                        print(f'Tableau : {e}')
    
    # Function for canvas with orange bar
    def canvas_with_orange_bar(canvas, doc):
        width, height = A4
        add_orange_bar(canvas, width, height)
    
    # Generate the PDF
    doc.build(elements, onFirstPage=canvas_with_orange_bar, onLaterPages=canvas_with_orange_bar)
    
    return output_filename

def create_pdf_jour(output_filename, contenu_jour, logo_path, formation_title, trainer_name):
    """
    Create a PDF presentation for multi-day content from the generated content
    
    Args:
        output_filename: Path to save the PDF file
        contenu_jour: Multi-day content structure with days, sessions, and subsections
        logo_path: Path to the logo image
        formation_title: Title of the presentation
        trainer_name: Name of the presenter
    """
    page_width, page_height = 600, 350
    
    doc = SimpleDocTemplate(output_filename, pagesize=(page_width, page_height),
                            leftMargin=15, rightMargin=15, topMargin=10, bottomMargin=15)
    
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    
    # Styles customization
    formation_style = ParagraphStyle(
        "FormationTitle",
        parent=styles["Title"],
        fontSize=45,
        textColor=colors.HexColor("#ff7900"),
        spaceAfter=15,
        spaceBefore=45,
        alignment=TA_LEFT,
    )
    
    trainer_style = ParagraphStyle(
        "TrainerName",
        parent=styles["BodyText"],
        fontSize=25,
        spaceAfter=45,
        spaceBefore=45,
        alignment=TA_CENTER,
        leftIndent=45,
    )
    
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=14,
        alignment=TA_LEFT,
        spaceAfter=5,
        spaceBefore=5,
        textColor=colors.HexColor("#ff7900")
    )
    
    day_title_style = ParagraphStyle(
        "DayTitleStyle",
        parent=styles["Title"],
        fontSize=20,
        alignment=TA_LEFT,
        spaceAfter=10,
        spaceBefore=10,
        textColor=colors.HexColor("#0097b2"),
        backgroundColor=colors.HexColor("#f3f3f3"),
        borderColor=colors.HexColor("#ff7900"),
        borderWidth=1,
        borderPadding=10,
        borderRadius=5
    )
    
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=17,
        spaceBefore=3,
        spaceAfter=3,
        rightIndent=15,
        fontName="Courier",
    )
    
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["BodyText"],
        fontSize=12,
        spaceAfter=2,
        textColor=colors.HexColor("#000"),
        leftIndent=15,
        fontName="Helvetica-Bold"
    )
    
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=20,
        spaceAfter=3,
        leftIndent=30,
        rightIndent=15,
        alignment=TA_JUSTIFY
    )
    
    elements = []
    
    # Function to add the orange bar
    def add_orange_bar(c, width, height):
        orange = colors.HexColor("#ff7900")
        c.setFillColor(orange)
        c.rect(-12, 0, 20, height, fill=True, stroke=False)
    
    # Check if logo exists, use placeholder if not
    if not os.path.exists(logo_path):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'default_logo.png')
        # If default logo doesn't exist either, create a blank image
        if not os.path.exists(logo_path):
            from PIL import Image as PILImage
            from PIL import ImageDraw
            img = PILImage.new('RGB', (150, 50), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((10, 20), "Logo", fill=(0, 0, 0))
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'default_logo.png')
            img.save(logo_path)
    
    # Add first page (Formation)
    img = Image(logo_path, width=120, height=30)
    img.hAlign = 'RIGHT'
    
    elements.append(img)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Formation", formation_style))
    elements.append(Paragraph(formation_title, trainer_style))
    elements.append(PageBreak())
    
    # Add second page (Presented by)
    elements.append(img)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Présenté par", formation_style))
    elements.append(Paragraph(trainer_name, trainer_style))
    elements.append(PageBreak())
    
    # Add table of contents 
    elements.append(Paragraph("Programme de la Formation", title_style))
    elements.append(Spacer(1, 20))
    
    # Loop through days for ToC
    for day_index, day_content in enumerate(contenu_jour):
        day_num = day_index + 1
        elements.append(Paragraph(f"Jour {day_num}:", subtitle_style))
        
        # Add session titles for each day in ToC
        for session_list in day_content:
            for session in session_list:
                session_title = session.get("title", "Sans titre")
                elements.append(Paragraph(f"• {session_title}", bullet_style))
        
        elements.append(Spacer(1, 10))
    
    elements.append(PageBreak())
    
    # Process each day's content
    for day_index, day_content in enumerate(contenu_jour):
        day_num = day_index + 1
        
        # Add day title
        elements.append(Paragraph(f"Jour {day_num}", day_title_style))
        elements.append(Spacer(1, 20))
        
        # Process each session in this day
        for session_list in day_content:
            for session in session_list:
                section_title = session.get("title", "Sans titre")
                elements.append(Paragraph(f"<b>{section_title}</b>", title_style))
                elements.append(Spacer(1, 10))
                
                # Handle subsections
                for subsection in session.get("subsections", []):
                    subsection_title = subsection.get("title", "Sous-section")
                    elements.append(Paragraph(f"{subsection_title}", subtitle_style))
                    elements.append(Spacer(1, 5))
                    
                    # Main content
                    content = subsection.get("content", "")
                    elements.append(Paragraph(content, body_style))
                    elements.append(Spacer(1, 10))
                    
                    # Example text if available
                    if "example" in subsection:
                        example_text = "Exemple: " + subsection["example"]
                        example_style = ParagraphStyle(
                            "ExampleStyle",
                            parent=body_style,
                            textColor=colors.HexColor("#006600"),
                            fontStyle='italic'
                        )
                        elements.append(Paragraph(example_text, example_style))
                        elements.append(Spacer(1, 5))
                    
                    # Bullet points
                    if "bullets" in subsection:
                        bullet_points = ListFlowable(
                            [ListItem(Paragraph(point, bullet_style)) for point in subsection["bullets"]],
                            bulletType="bullet",
                            leftIndent=25,
                            spaceBefore=5,
                            spaceAfter=5
                        )
                        elements.append(bullet_points)
                        elements.append(Spacer(1, 10))
                    
                    # Code blocks - handle both 'code' and 'code_example'
                    code_content = None
                    if "code" in subsection:
                        code_content = subsection["code"]
                    elif "code_example" in subsection:
                        code_content = subsection["code_example"]
                    
                    if code_content:
                        # Split by lines if it's a string
                        if isinstance(code_content, str):
                            code_lines = code_content.strip().split('\n')
                        else:
                            code_lines = code_content
                            
                        elements.append(format_code_block(code_lines))
                        elements.append(Spacer(1, 10))
                    
                    # Tables
                    if "table" in subsection:
                        table_data = subsection["table"]
                        elements.append(format_table(table_data))
                        elements.append(Spacer(1, 10))
                
                # Add more spacing between sections
                elements.append(Spacer(1, 20))
        
        # Add page break after each day except the last one
        if day_index < len(contenu_jour) - 1:
            elements.append(PageBreak())
    
    # Function for canvas with orange bar
    def canvas_with_orange_bar(canvas, doc):
        width, height = page_width, page_height
        add_orange_bar(canvas, width, height)
    
    # Generate the PDF
    doc.build(elements, onFirstPage=canvas_with_orange_bar, onLaterPages=canvas_with_orange_bar)
    
    return output_filename