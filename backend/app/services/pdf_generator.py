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
                if "code" in subsection:
                    elements.append(format_code_block(subsection["code"]))
                    elements.append(Spacer(1, 10))
                
                # Tables
                if "table" in subsection:
                    table_data = subsection["table"]
                    elements.append(format_table(table_data))
                    elements.append(Spacer(1, 10))
    
    # Function for canvas with orange bar
    def canvas_with_orange_bar(canvas, doc):
        width, height = A4
        add_orange_bar(canvas, width, height)
    
    # Generate the PDF
    doc.build(elements, onFirstPage=canvas_with_orange_bar, onLaterPages=canvas_with_orange_bar)
    
    return output_filename