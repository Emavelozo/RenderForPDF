from flask import Flask, request, send_file
from weasyprint import HTML, CSS
import io
import json

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_html_to_pdf():
    try:
        data = request.get_json()
        html_content = data.get('html')
        filename = data.get('filename', 'document.pdf')
        
        if not html_content:
            return {'error': 'HTML content is required'}, 400
        
        # Convert HTML to PDF
        html_doc = HTML(string=html_content)
        pdf_bytes = html_doc.write_pdf()
        
        # Create file-like object
        pdf_io = io.BytesIO(pdf_bytes)
        pdf_io.seek(0)
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
