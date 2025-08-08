# ultaPDF - 500 Files PDF Merge Backend (Flask)

from flask import Flask, request, send_file, jsonify, render_template
from PyPDF2 import PdfMerger
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
MERGED_FOLDER = 'temp_outputs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({'error': 'No files selected for uploading'}), 400

    if len(files) > 500:
        return jsonify({'error': 'Maximum 500 files allowed'}), 400

    merger = PdfMerger()
    saved_files = []

    try:
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            merger.append(filepath)
            saved_files.append(filepath)

        unique_filename = f'merged_{uuid.uuid4().hex}.pdf'
        output_pdf_path = os.path.join(MERGED_FOLDER, unique_filename)
        merger.write(output_pdf_path)
        merger.close()

        # Cleanup uploaded files
        for file_path in saved_files:
            os.remove(file_path)

        return send_file(output_pdf_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
