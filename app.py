from flask import Flask, request, send_file
from fpdf import FPDF
import tempfile
import os

app = Flask(__name__)

# Constants
FONT_NAME = 'Handwriting'
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'Handwriting.ttf')

class RuledPDF(FPDF):
    def header(self):
        self.set_draw_color(200, 200, 200)  # light gray for ruled lines
        for y in range(40, 290, 10):  # leave space for heading (starts at y=40)
            self.line(20, y, 200, y)

        # Draw two vertical margin lines (1 inch = ~25.4 mm ≈ 28 px)
        self.set_draw_color(180, 180, 180)
        self.line(38, 10, 38, 290)  # Left vertical line
        self.line(43, 10, 43, 290)  # Right vertical line

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    text = data.get('text', 'No text provided.')

    pdf = RuledPDF()
    pdf.add_page()

    try:
        pdf.add_font(FONT_NAME, '', FONT_PATH, uni=True)
        pdf.set_font(FONT_NAME, '', 14)
    except Exception as e:
        print(f"Error loading custom font: {e}")
        pdf.set_font('Arial', '', 14)

    pdf.set_text_color(0, 0, 255)  # Blue font

    # Set initial position (after heading space + margin)
    pdf.set_xy(45, 40)
    pdf.multi_cell(0, 10, text)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp.name)
    tmp.close()

    return send_file(tmp.name, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
