from .base_report import BaseReport
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class MicroalbuminReport(BaseReport):
    def __init__(self, buffer, microalbumin_test):
        super().__init__(buffer)
        self.microalbumin_test = microalbumin_test

    def add_test_details(self):
        """Add Microalbumin test details to the PDF."""
        test_data = [
            ["Test ID", str(self.microalbumin_test.test_id)],
            ["Test Date", self.microalbumin_test.test_date.strftime("%Y-%m-%d")],
            ["Colour", self.microalbumin_test.colour],
            ["Clarity", self.microalbumin_test.clarity],
            ["Albumin", self.microalbumin_test.albumin],
            ["Creatine", self.microalbumin_test.creatine],
            ["AC Ratio", self.microalbumin_test.acratio],
            ["Other Test", self.microalbumin_test.other_test],
            ["Result", self.microalbumin_test.result],
            ["Remark", self.microalbumin_test.remark],
        ]
        test_table = Table(test_data, colWidths=[150, 250])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        self.elements.append(test_table)

    def generate(self, pathology_info):
        """Generate the complete PDF report."""
        self.add_logo()
        self.add_header(pathology_info)
        self.add_patient_details(self.microalbumin_test.patient)
        self.add_test_details()
        return self.build_pdf()