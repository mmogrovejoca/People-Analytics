from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Análisis de Rotación', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_image_from_fig(self, fig, title):
        self.chapter_title(title)

        # Guardar la figura en un archivo temporal para poder insertarla en el PDF
        temp_image_path = 'temp_plot.png'
        fig.savefig(temp_image_path)

        self.image(temp_image_path, x=10, w=190)
        self.ln(5)

        # Limpiar el archivo temporal
        import os
        os.remove(temp_image_path)

def generate_pdf_report(data, metrics, figures):
    """
    Genera un reporte en PDF con los datos, métricas y gráficos.

    Args:
        data (pandas.DataFrame): DataFrame con los datos de los empleados.
        metrics (dict): Diccionario con las métricas calculadas.
        figures (dict): Diccionario con las figuras de Matplotlib.

    Returns:
        bytes: El contenido del PDF en bytes.
    """
    pdf = PDF()
    pdf.add_page()

    # Resumen de Métricas
    pdf.chapter_title('Resumen de Métricas')
    for key, value in metrics.items():
        pdf.chapter_body(f"{key}: {value}")

    # Gráficos
    for title, fig in figures.items():
        pdf.add_image_from_fig(fig, title)
        pdf.add_page()

    return pdf.output(dest='S').encode('latin-1')
