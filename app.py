
from flask import Flask, request, send_file
from fpdf import FPDF
import tempfile
import os

app = Flask(__name__)

class RuledPDF(FPDF):
    def header(self):
        self.set_draw_color(200, 200, 200)
        for y in range(20, 290, 10):
            self.line(10, y, 200, y)

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    text = data.get('text', '')

    pdf = RuledPDF()
    pdf.add_page()
    try:
        pdf.add_font('Lucida', '', 'LucidaHandwriting.ttf', uni=True)
        pdf.set_font('Lucida', '', 14)
    except:
        pdf.set_font('Arial', '', 14)
    pdf.multi_cell(0, 10, text)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp.name)
    return send_file(tmp.name, as_attachment=False, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
