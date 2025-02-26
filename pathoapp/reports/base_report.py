from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

class BaseReport:
    def __init__(self, buffer, pagesize=letter):
        self.buffer = buffer
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self.elements = []

    def add_logo(self):
        """Add the pathology center logo to the PDF."""
        logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'logo.jpeg')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=100, height=100)
            self.elements.append(logo)
        else:
            self.elements.append(Paragraph("Logo not found", self.styles['Normal']))

    def add_header(self, pathology_info):
        """Add the pathology center information to the PDF."""
        if pathology_info:
            header_data = [
                [pathology_info.name],
                [f"Address: {pathology_info.add1}, {pathology_info.add2}, {pathology_info.city}"],
                [f"Mobile: {pathology_info.mobile}"],
            ]
            header_table = Table(header_data, colWidths=[400])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
            ]))
            self.elements.append(header_table)

    def add_patient_details(self, patient):
        """Add patient details to the PDF in horizontal format."""
        # Define the headers and data in a single row
        headers = ["Patient Name", "Age", "Gender", "Mobile", "Email"]
        patient_data = [
            patient.patientname,
            str(patient.age),
            patient.gender,
            patient.mobile,
            patient.email if patient.email else "N/A",
        ]

        # Create a table with headers and data in a single row
        patient_table = Table([headers, patient_data], colWidths=[100, 50, 50, 100, 150])
        
        # Apply table styles
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header row font
            ('FONTSIZE', (0, 0), (-1, -1), 10),                # Font size for all cells
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),      # Grid lines
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),             # Center align all cells
        ]))
        
        # Add the table to the elements list
        self.elements.append(patient_table)

    def build_pdf(self):
        """Generate the PDF and return the buffer."""
        pdf = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)
        pdf.build(self.elements)
        return self.buffer