from .base_report import BaseReport
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class BloodSugarReport(BaseReport):
    def __init__(self, buffer, bloodsugar_test):
        super().__init__(buffer)
        self.bloodsugar_test = bloodsugar_test

    def add_test_details(self):
        """Add Blood Sugar test details to the PDF."""
        test_data = [
            ["Test ID", str(self.bloodsugar_test.test_id)],
            ["Test Date", self.bloodsugar_test.test_date.strftime("%Y-%m-%d")],
            ["Blood Sugar (Fasting)", f"{self.bloodsugar_test.bloodfas} mg/dL"],
            ["Blood Sugar (PP)", f"{self.bloodsugar_test.bloodpp} mg/dL"],
            ["Blood Sugar (Random)", f"{self.bloodsugar_test.bloodrandom} mg/dL"],
            ["Urine Sugar (Fasting)", self.bloodsugar_test.urinefas],
            ["Urine Sugar (PP)", self.bloodsugar_test.urinepp],
            ["Urine Sugar (Random)", self.bloodsugar_test.urinerandom],
            ["Acetone", self.bloodsugar_test.acetone],
            ["Other Test", self.bloodsugar_test.other_test],
            ["Result", self.bloodsugar_test.result],
            ["Remarks", self.bloodsugar_test.remarks],
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
        self.add_patient_details(self.bloodsugar_test.patient)
        self.add_test_details()
        return self.build_pdf()
