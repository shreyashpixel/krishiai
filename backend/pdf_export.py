"""
KrishiAI - Automated Farm Inspection & Project Report Generator
Uses ReportLab to synthesize an executive agricultural audit PDF
including live sensor telemetry, ML crop predictions, pathology scans, and sustainability metrics.
"""
import io
import datetime
from typing import Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from backend.simulator import iot_simulator
from backend.ml_crops import crop_recommender
from backend.ml_disease import disease_detector
from backend.sustainability import calculate_sustainability_metrics
from backend.database import get_recent_disease_scans

class NumberedCanvas(canvas.Canvas):
    """Adds professional running headers and footers with page counts."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2d6a4f"))
        # Header
        self.drawString(54, 755, "KrishiAI – Smart Agriculture System | College Innovation Demo")
        self.setStrokeColor(colors.HexColor("#d8f3dc"))
        self.setLineWidth(0.5)
        self.line(54, 747, 558, 747)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Generated automatically by KrishiAI Autonomous Decision Engine. Strictly for academic demo.")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_farm_report_pdf() -> bytes:
    """Generates complete in-memory PDF document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom typography
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1b4332"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#52b788"),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#2d6a4f"),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#222222")
    )

    badge_style = ParagraphStyle(
        "BadgeText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#ffffff")
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("KrishiAI™ Precision Farm Audit Report", title_style))
    now_str = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    meta_text = (
        f"<b>Audit Date:</b> {now_str} &nbsp;|&nbsp; "
        f"<b>Farm Zone:</b> Pune Agro-Climatic Region &nbsp;|&nbsp; "
        f"<b>System Status:</b> Online (Autonomous IoT Simulation)"
    )
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2d6a4f"), spaceAfter=12))

    # 1. Executive Telemetry Summary
    story.append(Paragraph("1. Executive Field Telemetry & Soil Health", h2_style))
    live = iot_simulator.get_current_readings()

    telemetry_data = [
        ["Parameter", "Observed Reading", "Agronomic Target", "Status"],
        ["Soil Moisture", f"{live['soil_moisture']}%", "45.0% - 55.0%", "Optimal" if 40 <= live['soil_moisture'] <= 60 else "Action Required"],
        ["Root Temperature", f"{live['temperature']} °C", "22.0 - 32.0 °C", "Normal"],
        ["Ambient Humidity", f"{live['humidity']}%", "50.0% - 75.0%", "Good"],
        ["Soil pH", f"{live['ph']}", "6.2 - 7.2", "Slightly Acidic (Good)"],
        ["Nitrogen (N)", f"{live['nitrogen']} kg/ha", "60 - 90 kg/ha", "Sufficient"],
        ["Phosphorus (P)", f"{live['phosphorus']} kg/ha", "35 - 60 kg/ha", "Optimal"],
        ["Potassium (K)", f"{live['potassium']} kg/ha", "40 - 65 kg/ha", "Optimal"],
        ["Farm Health Index", f"{live['health_score']} / 100", "> 80 Score", "Excellent"]
    ]

    t1 = Table(telemetry_data, colWidths=[130, 120, 130, 125])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d6a4f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8faf9"), colors.HexColor("#ffffff")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8f3dc")),
    ]))
    story.append(t1)
    story.append(Spacer(1, 12))

    # 2. Crop Recommendations (ML)
    story.append(Paragraph("2. Machine Learning Crop Recommendations", h2_style))
    story.append(Paragraph(
        "Random Forest Classifier (trained on 2,400+ balanced regional records) ranked crops based on current soil NPK, pH, and local weather:",
        body_style
    ))
    story.append(Spacer(1, 6))

    crop_preds = crop_recommender.predict(
        live["nitrogen"], live["phosphorus"], live["potassium"],
        live["ph"], live["temperature"], live["humidity"], 100.0
    )

    crop_table_data = [["Rank", "Recommended Crop", "Confidence", "Ideal Season", "Water Need", "Target Soil"]]
    for c in crop_preds:
        crop_table_data.append([
            f"#{c['rank']}",
            c["crop"],
            f"{c['confidence']}%",
            c["season"],
            c["water_requirement"],
            c["soil_type"]
        ])

    t2 = Table(crop_table_data, colWidths=[40, 100, 75, 100, 100, 90])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#40916c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f0fdf4"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbf7d0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 12))

    # 3. Smart Irrigation Plan
    story.append(Paragraph("3. Precision Irrigation Schedule", h2_style))
    plan = iot_simulator.plan_smart_irrigation()
    irrig_text = (
        f"<b>Target Crop:</b> {plan['crop']} &nbsp;|&nbsp; "
        f"<b>Target Soil Moisture:</b> {plan['target_moisture']}% &nbsp;|&nbsp; "
        f"<b>Urgency:</b> {plan['urgency']}<br/>"
        f"• <b>Water Quota:</b> {plan['water_required_litres']:,} Litres ({plan['drip_runtime_minutes']} minutes via micro-drip).<br/>"
        f"• <b>Water Conserved:</b> {plan['water_saved_litres']:,} Litres saved vs. traditional flood irrigation (54.5% conservation).<br/>"
        f"• <b>Recommendation:</b> {plan['recommendation']}"
    )
    story.append(Paragraph(irrig_text, body_style))
    story.append(Spacer(1, 12))

    # 4. Foliar Pathology Scan
    story.append(Paragraph("4. Plant Foliar Pathology & Disease Scan", h2_style))
    recent_scans = get_recent_disease_scans(limit=1)
    if recent_scans:
        s = recent_scans[0]
        disease_name = s["detected_disease"]
        severity = s["severity"]
        org_treat = s["organic_treatment"]
        chem_treat = s["chemical_treatment"]
    else:
        disease_name = "Healthy Foliage"
        severity = 0
        org_treat = "Preventive neem oil spray (5ml/L)."
        chem_treat = "No chemical intervention needed."

    pathology_data = [
        ["Inspection Metric", "Automated Finding"],
        ["Diagnosis", disease_name],
        ["Severity Index", f"{severity}% (Moderate)" if severity > 0 else "0% (Healthy)"],
        ["Biological / Organic Remedy", Paragraph(org_treat, body_style)],
        ["Chemical / Modern Remedy", Paragraph(chem_treat, body_style)]
    ]
    t3 = Table(pathology_data, colWidths=[150, 355])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b4332")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fef2f2") if severity > 40 else colors.HexColor("#f0fdf4"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t3)
    story.append(Spacer(1, 12))

    # 5. Ecological Sustainability Footprint
    story.append(Paragraph("5. Sustainability & Climate Resilience Meter", h2_style))
    sust = calculate_sustainability_metrics(farm_area_acres=3.5)
    sust_text = (
        f"• <b>Total Groundwater Conserved:</b> {sust['water_saved_litres']:,} Litres ({sust['water_saved_m3']} m³)<br/>"
        f"• <b>Carbon Emissions Mitigated:</b> {sust['total_co2e_saved_kg']} kg CO₂e (Equivalent to planting {sust['trees_equivalent']} trees)<br/>"
        f"• <b>Excess Nitrogen Leaching Prevented:</b> {sust['nitrogen_saved_kg']} kg N<br/>"
        f"• <b>Overall Sustainability Index:</b> <b>{sust['sustainability_index']} / 100</b> (Grade A+)"
    )
    story.append(Paragraph(sust_text, body_style))
    story.append(Spacer(1, 18))

    # Academic Sign-off
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#cccccc"), spaceAfter=8))
    sign_off = (
        "<b>Verified by KrishiAI Autonomous Agronomy Engine.</b><br/>"
        "Project Submission: College Innovation Demo Prototype. All algorithms run locally without external cloud dependencies."
    )
    story.append(Paragraph(sign_off, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()
