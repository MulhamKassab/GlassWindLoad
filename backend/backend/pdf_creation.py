from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# === Define Colors ===
logo_red = HexColor('#DF0029')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyBold', fontName='Helvetica-Bold', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MyNormal', fontName='Helvetica', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MainTitle', fontName='Helvetica-Bold', fontSize=18, textColor=logo_red, alignment=TA_LEFT, spaceAfter=20))
styles.add(ParagraphStyle(name='SecondTitle', fontName='Helvetica-Bold', fontSize=14, textColor=black, alignment=TA_LEFT, spaceAfter=15))
styles.add(ParagraphStyle(name='MySubTitle', fontName='Helvetica-Bold', fontSize=10, textColor=logo_red, alignment=TA_LEFT, spaceAfter=7))
styles.add(ParagraphStyle(name='MySection', fontName='Helvetica-Bold', fontSize=10, textColor=black, spaceAfter=8))

def draw_section_title(text):
    title_data = [[text]]
    table = Table(title_data, colWidths=[480])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#FF0000")),
        ('TEXTCOLOR', (0, 0), (-1, -1), white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    return table

def draw_paragraph(text, style):
    return Paragraph(text, style)

def add_logo_and_text(canvas, doc, logo_path):
    logo = Image(logo_path, width=70, height=70)
    logo.drawOn(canvas, doc.pagesize[0] - 130, doc.pagesize[1] - 80)

    canvas.setFont('Helvetica', 10)
    footer = """Dubai Investment Park 2
P.O. Box 54563,
Dubai, UAE
+971 4 88 5333 6
info@gutmannpvb.com
www.gutmannpvb.com"""
    for i, line in enumerate(footer.split("\n")):
        canvas.drawString(40, 20 + (12 * i), line)

# === Glass Spec Drawing ===
def draw_glass_spec_table(thicknesses, plyThicknessList, pvb_thicknesses, glass_layers_strength_type, heat_treatments):
    from reportlab.lib.colors import HexColor
    row_data = []
    layer_colors = []
    heat_treatment_colors = {
        'annealed': HexColor("#B3E5FC"),
        'tempered': HexColor("#FFCDD2"),
        'heatStrengthened': HexColor("#C8E6C9"),
        'default': HexColor("#E0E0E0")
    }

    for i, typ in enumerate(glass_layers_strength_type):
        if typ == 'mono':
            row_data.append(thicknesses[i])
            layer_colors.append(heat_treatment_colors.get(heat_treatments[i], heat_treatment_colors['default']))
        elif typ == 'laminated':
            ply_index = 0
            for ply in plyThicknessList:
                row_data.append(ply)
                layer_colors.append(heat_treatment_colors.get(heat_treatments[i], heat_treatment_colors['default']))
                if ply_index < len(pvb_thicknesses):
                    row_data.append(pvb_thicknesses[ply_index])
                    layer_colors.append(heat_treatment_colors['default'])
                    ply_index += 1

    col_widths = [max(20, min(float(val) * 10, 100)) for val in row_data]
    spec_table = Table([row_data], colWidths=col_widths, rowHeights=[100])

    style = [
        ('BACKGROUND', (i, 0), (i, 0), layer_colors[i])
        for i in range(len(row_data))
    ] + [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0, colors.white),
        ('LINEABOVE', (0, 0), (-1, -1), 0, colors.white),
        ('LINEBEFORE', (0, 0), (-1, -1), 0, colors.white),
        ('LINEAFTER', (0, 0), (-1, -1), 0, colors.white)
    ]

    spec_table.setStyle(TableStyle(style))
    return spec_table

# === PDF Builder ===
def create_pdf(fileobj, glass_length, glass_width, pvb_thicknesses, number_of_supported_sides, thicknesses,
               plyThicknessList, glass_weight, short_load, long_load, allowable_Deflection, lr, short_cof, long_cof,
               glass_layers_strength_type, heat_treatments, logo_path, first_page_image_path):

    if glass_width > glass_length:
        glass_length, glass_width = glass_width, glass_length

    doc = SimpleDocTemplate(fileobj, pagesize=A4, topMargin=30)
    elements = []

    # Cover Page
    elements += [
        PageBreak(),
        draw_paragraph("GUTMANN PVB", styles['MainTitle']),
        draw_paragraph("Load Resistance Report", styles['SecondTitle']),
        draw_paragraph("Based on ASTM E1300", styles['MyNormal']),
        Spacer(1, 20),
    ]

    # Glass Spec Table
    spec_table = draw_glass_spec_table(thicknesses, plyThicknessList, pvb_thicknesses, glass_layers_strength_type, heat_treatments)
    info_table = Table([[draw_paragraph(f"<b>Long side (mm):</b> {glass_length}", styles['MyNormal']),
                         draw_paragraph(f"<b>Supported sides:</b> {number_of_supported_sides}", styles['MyNormal']),
                         draw_paragraph(f"<b>Allowable deflection (mm):</b> {allowable_Deflection}", styles['MyNormal']),
                         draw_paragraph(f"<b>Glass weight (KG):</b> {glass_weight}", styles['MyNormal']),
                         spec_table]],
                       colWidths=[150, 150, 150, 150, 150], hAlign="LEFT")
    info_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Layers
    for i, (t, l, h) in enumerate(zip(thicknesses, glass_layers_strength_type, heat_treatments)):
        elements.append(draw_paragraph(f"Layer {i + 1}:", styles['MySubTitle']))
        elements.append(draw_paragraph(f"<b>Thickness:</b> {t} mm, <b>Lite Type:</b> {l}, <b>Heat Treatment:</b> {h}", styles['MyNormal']))

    # Loads
    elements += [
        Spacer(1, 12),
        draw_paragraph("Applied Loads:", styles['MySubTitle']),
        draw_paragraph(f"<b>Short Duration Load:</b> {short_load} kPa (3 sec)", styles['MyNormal'])
    ]
    if long_load > 0:
        elements.append(draw_paragraph(f"<b>Long Duration Load:</b> {long_load} kPa (30 days)", styles['MyNormal']))
    elements.append(Spacer(1, 12))

    # Final Results
    elements.append(draw_section_title("Final Results:"))
    elements.append(Spacer(1, 12))

    def build_result_table(title, headers, rows):
        table = Table([headers] + rows, hAlign="LEFT")
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DF0029')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('BACKGROUND', (1, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ]))
        return table

    # === LR Table
    lr_table_data = [["Layer", "Duration", "LR (kPa)", "Applied Load (kPa)", "Result"]]
    for i in range(len(thicknesses)):
        short_lr = lr[0]["short"][i]
        short_result = "Accepted" if short_lr > short_load else "Not Accepted"
        lr_table_data.append([f"{i+1}", "Short", f"{short_lr:.2f}", f"{short_load:.2f}", short_result])
        if long_load > 0:
            long_lr = lr[0]["long"][i]
            long_result = "Accepted" if long_lr > long_load else "Not Accepted"
            lr_table_data.append(["", "Long", f"{long_lr:.2f}", f"{long_load:.2f}", long_result])
    elements.append(build_result_table("LR", *zip(*lr_table_data)))

    # === COF Table
    cof_table_data = [["Layer", "Duration", "Deflection (mm)", "Allowable (mm)", "Result"]]
    for i in range(len(thicknesses)):
        short_result = "Accepted" if short_cof[i] < allowable_Deflection else "Not Accepted"
        cof_table_data.append([f"{i+1}", "Short", f"{short_cof[i]:.2f}", f"{allowable_Deflection:.2f}", short_result])
        if long_load > 0:
            long_result = "Accepted" if long_cof[i] < allowable_Deflection else "Not Accepted"
            cof_table_data.append(["", "Long", f"{long_cof[i]:.2f}", f"{allowable_Deflection:.2f}", long_result])
    elements.append(Spacer(1, 12))
    elements.append(build_result_table("COF", *zip(*cof_table_data)))

    # Render PDF
    doc.build(elements,
              onFirstPage=lambda canvas, doc: canvas.drawImage(first_page_image_path, 0, 0, width=A4[0], height=A4[1]),
              onLaterPages=lambda canvas, doc: add_logo_and_text(canvas, doc, logo_path))
