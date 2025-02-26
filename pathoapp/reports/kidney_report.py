from .base_report import BaseReport
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class KidneyReport(BaseReport):
    def __init__(self, buffer, kidney_test):
        super().__init__(buffer)
        self.kidney_test = kidney_test

    def add_test_details(self):
        """Add Kidney test details to the PDF."""
        test_data = [
            ["Test ID", str(self.kidney_test.test_id)],
            ["Test Date", self.kidney_test.test_date.strftime("%Y-%m-%d")],
            ["Blood Urea", f"{self.kidney_test.bloodurea} mg/dL"],
            ["Serum Creatinine", f"{self.kidney_test.serumcreatinine} mg/dL"],
            ["BUN", f"{self.kidney_test.bun} mg/dL"],
            ["Uric Acid", f"{self.kidney_test.uricacid} mg/dL"],
            ["Other Test", self.kidney_test.other_test],
            ["Result", self.kidney_test.result],
            ["Normal Value", self.kidney_test.normal_value],
            ["Remarks", self.kidney_test.remarks],
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
        self.add_patient_details(self.kidney_test.patient)
        self.add_test_details()
        return self.build_pdf()