from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import os
from pathlib import Path
from werkzeug.utils import secure_filename

# Flask config
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'pdf'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

USERS = {'admin': 'admin', 'user': 'user'}  # replace with secure storage for production

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Main:
    def __init__(self, upload_dir=UPLOAD_FOLDER, max_files=6):
        self.upload_dir = upload_dir
        self.max_files = max_files
        os.makedirs(self.upload_dir, exist_ok=True)

    def get_uploaded_files(self):
        return [f for f in os.listdir(self.upload_dir) if f.lower().endswith('.mp4')]

    def get_uploaded_pdfs(self):
        return [f for f in os.listdir(self.upload_dir) if f.lower().endswith('.pdf')]

    def delete_file(self, file_name):
        file_path = os.path.join(self.upload_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False


main = Main()


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    uploaded_files = main.get_uploaded_files()
    uploaded_pdfs = main.get_uploaded_pdfs()
    return render_template('index.html', files=uploaded_files, pdfs=uploaded_pdfs, username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session or session.get('username') != 'admin':
        flash('Permission denied', 'danger')
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('No file part', 'warning')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(dest):
            flash('Erro: arquivo já existe.', 'warning')
            return redirect(url_for('index'))

        # Se for vídeo, respeitar limite de vídeos
        if filename.lower().endswith('.mp4'):
            uploaded_videos = main.get_uploaded_files()
            if len(uploaded_videos) >= main.max_files:
                flash(f'Erro: limite de {main.max_files} vídeos atingido.', 'danger')
                return redirect(url_for('index'))

        try:
            file.save(dest)
            flash('Arquivo enviado com sucesso.', 'success')
        except Exception as e:
            flash(f'Erro ao salvar arquivo: {e}', 'danger')
        return redirect(url_for('index'))
    else:
        flash('Erro: apenas arquivos .mp4 e .pdf são permitidos.', 'danger')
        return redirect(url_for('index'))


@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if 'username' not in session or session.get('username') != 'admin':
        flash('Permission denied', 'danger')
        return redirect(url_for('index'))
    filename = secure_filename(filename)
    if main.delete_file(filename):
        flash('Arquivo excluído.', 'success')
    else:
        flash('Arquivo não encontrado.', 'warning')
    return redirect(url_for('index'))


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Para testes locais
    app.run(debug=True)