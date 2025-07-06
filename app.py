from flask import Flask, request, send_file
from fpdf import FPDF
import tempfile
import os

app = Flask(__name__)

# Path to your handwriting font
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'Handwriting.ttf')

class RuledPDF(FPDF):
    def header(self):
        # Draw faint ruled lines on the page
        self.set_draw_color(200, 200, 200)
        for y in range(20, 290, 10):
            self.line(10, y, 200, y)

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    text = data.get('text', 'No text provided.')

    pdf = RuledPDF()
    pdf.add_page()

    try:
        # Register and set your custom handwriting font
        pdf.add_font('Handwriting', '', FONT_PATH, uni=True)
        pdf.set_font('Handwriting', '', 14)
    except Exception as e:
        print(f"Error loading custom font: {e}")
        pdf.set_font('Arial', '', 14)

    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, text)

    # Save the PDF to a temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp.name)
    tmp.close()

    return send_file(tmp.name, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

