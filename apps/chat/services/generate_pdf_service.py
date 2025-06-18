import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# Kirillcha (ruscha/o'zbekcha) shriftni ro‘yxatdan o‘tkazamiz
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

def generate_wrapped_pdf(text):
    buffer = io.BytesIO()

    # PDF faylni yaratamiz
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    # Stil sozlamalari (Paragraph uchun)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "DejaVu"
    style.fontSize = 12
    style.leading = 16  # qatorlar oraliqligi

    # Matnni Paragraph shaklida o‘rab qo‘yamiz
    story = []
    for paragraph in text.split("\n"):
        story.append(Paragraph(paragraph.strip(), style))
        story.append(Spacer(1, 0.5*cm))  # paragraf orasida bo‘sh joy

    # PDF generatsiya
    doc.build(story)
    buffer.seek(0)
    return buffer
