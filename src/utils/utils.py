from fpdf import FPDF

class ReportPDF(FPDF):
    """PDF generation class with header and footer."""
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Sales Insights Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


class Scraper:
    def __init__(self, config: dict):
        self.config = config

    def scrape(self):
        # Scrape the website
        pass

    def save(self):
        # Save the scraped data
        pass

    def run(self):
        self.scrape()
        self.save()