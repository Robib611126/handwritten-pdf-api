from flask import Flask, request, send_file
from fpdf import FPDF
import tempfile
import os

app = Flask(__name__)

# Path to font
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'Handwriting.ttf')

class RuledPDF(FPDF):
    def header(self):
        # Ruled lines (notebook style)
        self.set_draw_color(200, 200, 200)
        for y in range(40, 290, 10):  # start after heading space
            self.line(25, y, 200, y)

        # Two vertical lines at 1-inch margin (approx 25mm)
        self.line(25, 20, 25, 290)  # red line
        self.line(30, 20, 30, 290)  # blue line

@app.route('/generate', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        text = data.get('text', 'No text provided.')
        print("[Received Text]:", text)

        pdf = RuledPDF()
        pdf.add_page()

        # Set font
        try:
            pdf.add_font('Handwriting', '', FONT_PATH, uni=True)
            pdf.set_font('Handwriting', '', 14)
        except Exception as font_error:
            print(f"[Font Error]: {font_error}")
            pdf.set_font('Arial', '', 14)

        # Blue text
        pdf.set_text_color(0, 0, 255)

        # Start writing from top margin
        pdf.set_xy(35, 40)  # position right after header margin
        pdf.multi_cell(0, 10, text)

        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf.output(tmp.name)
        tmp.close()

        return send_file(tmp.name, mimetype='application/pdf')

    except Exception as e:
        print(f"[Server Error]: {e}")
        return {"error": "Internal Server Error", "details": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
