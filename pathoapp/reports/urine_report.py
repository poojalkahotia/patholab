from .base_report import BaseReport
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class UrineReport(BaseReport):
    def __init__(self, buffer, urine_test):
        super().__init__(buffer)
        self.urine_test = urine_test

    def add_test_details(self):
        """Add Urine test details to the PDF."""
        test_data = [
            ["Test ID", str(self.urine_test.test_id)],
            ["Test Date", self.urine_test.test_date.strftime("%Y-%m-%d")],
            ["Colour", self.urine_test.colour],
            ["Appearance", self.urine_test.appearance],
            ["Sediment", self.urine_test.sediment],
            ["Reaction", self.urine_test.reaction],
            ["Albumin", self.urine_test.albumin],
            ["Sugar", self.urine_test.sugar],
            ["Pus Cells", self.urine_test.puscells],
            ["RBC", self.urine_test.rbc],
            ["Epithelial Cells", self.urine_test.epithelialcells],
            ["Bile Salt", self.urine_test.bilesalt],
            ["Acetone", self.urine_test.aceyone],
            ["Bile Pigment", self.urine_test.bilepigment],
            ["Occult Blood", self.urine_test.occultblood],
            ["Casts", self.urine_test.casts],
            ["Crystals", self.urine_test.crystals],
            ["Microorganism", self.urine_test.microorganism],
            ["Other Test", self.urine_test.other_test],
            ["Other Test Result", self.urine_test.other_test_result],
            ["Remarks", self.urine_test.remarks],
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
        self.add_patient_details(self.urine_test.patient)
        self.add_test_details()
        return self.build_pdf()