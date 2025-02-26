from .base_report import BaseReport
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class HivReport(BaseReport):
    def __init__(self, buffer, hiv_test):
        super().__init__(buffer)
        self.hiv_test = hiv_test

    def add_test_details(self):
        """Add HIV test details to the PDF."""
        test_data = [
            ["Test ID", str(self.hiv_test.test_id)],
            ["Test Date", self.hiv_test.test_date.strftime("%Y-%m-%d")],
            ["HIV Test", self.hiv_test.hiv],
            ["Other Test", self.hiv_test.other_test],
            ["Result", self.hiv_test.result],
            ["Normal Value", self.hiv_test.normal_value],
            ["Remarks", self.hiv_test.remarks],
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
        self.add_patient_details(self.hiv_test.patient)
        self.add_test_details()
        return self.build_pdf()