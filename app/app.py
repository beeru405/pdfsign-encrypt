from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    bank_id = request.form.get('bank_id')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and bank_id:
        bank_id_folder = os.path.join(UPLOAD_FOLDER, bank_id)
        os.makedirs(bank_id_folder, exist_ok=True)

        bank_id_file_path = os.path.join(bank_id_folder, 'bankid.key')
        try:
            with open(bank_id_file_path, 'w') as bank_id_file:
                bank_id_file.write(bank_id)
        except Exception as e:
            return jsonify({'error': f'Failed to write bankid.key: {str(e)}'}), 500

        filename = secure_filename(file.filename)
        file_path = os.path.join(bank_id_folder, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

        return jsonify({'message': 'File uploaded and Bank ID stored successfully'}), 200

@app.route('/sign', methods=['POST'])
def sign_file():
    bank_id = request.form.get('bank_id')
    if not bank_id:
        return jsonify({'error': 'No Bank ID provided'}), 400

    bank_id_folder = os.path.join(UPLOAD_FOLDER, bank_id)
    if not os.path.exists(bank_id_folder):
        return jsonify({'error': 'Bank ID folder does not exist'}), 400

    pdf_file_path = os.path.join(bank_id_folder, 'your_uploaded_pdf.pdf')  # Adjust filename as needed
    signed_pdf_path = os.path.join(bank_id_folder, 'signed_pdf.pdf')
    key_file_path = os.path.join(bank_id_folder, 'privkey1.out')
    sig_file_path = os.path.join(bank_id_folder, 'signature123.sign')

    try:
        subprocess.run(['python3', 'sign_pdf.py', key_file_path, pdf_file_path, sig_file_path, signed_pdf_path], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Signing failed: {str(e)}'}), 500

    return jsonify({'message': 'File signed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
