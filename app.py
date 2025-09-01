import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

# --- 1. CONFIGURAÇÃO INICIAL ---

# Define a pasta onde os arquivos enviados serão armazenados
UPLOAD_FOLDER = 'uploads'
# Define as extensões de arquivo que são permitidas
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'ofx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Chave secreta necessária para usar 'flash messages' (mensagens de feedback)
app.config['SECRET_KEY'] = 'sua-chave-secreta-super-dificil' 

# --- 2. FUNÇÃO AUXILIAR ---

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 3. ROTAS PARA CADA PÁGINA HTML ---

# Rota para a página de Login (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de Cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota para o Dashboard
@app.route('/dashboard')
def dashboard():
    # No futuro, aqui você vai carregar os dados do usuário do banco de dados
    return render_template('dashboard.html')

# Rota para a página de Upload (GET)
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# Rota para registrar despesa
@app.route('/despesa')
def despesa():
    return render_template('despesa.html')

# Rota para registrar receita
@app.route('/receita')
def receita():
    return render_template('receita.html')

# Rota para o simulador
@app.route('/simulador')
def simulador():
    return render_template('simulador.html')

# Rota para criar meta
@app.route('/meta')
def meta():
    return render_template('meta.html')

# Rota para o perfil
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# --- 4. LÓGICA PRINCIPAL: UPLOAD DO ARQUIVO (POST) ---

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica se a requisição contém a parte do arquivo
    if 'extrato' not in request.files:
        flash('Erro: Nenhuma parte do arquivo na requisição.')
        return redirect(url_for('upload_page'))

    file = request.files['extrato']

    # Se o usuário não selecionar um arquivo, o navegador
    # envia uma parte vazia sem nome de arquivo.
    if file.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('upload_page'))

    # Se o arquivo existir e tiver uma extensão permitida...
    if file and allowed_file(file.filename):
        # secure_filename garante que o nome do arquivo não é malicioso
        filename = secure_filename(file.filename)
        
        # Garante que a pasta de uploads exista
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        # Salva o arquivo na pasta de uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- É AQUI QUE A ANÁLISE DO EXTRATO COMEÇARÁ ---
        # Por enquanto, apenas mostramos uma mensagem de sucesso.
        # Futuramente, você chamará sua função de processamento aqui.
        # Ex: dados_extraidos = processar_extrato(filepath)
        
        flash(f"Arquivo '{filename}' enviado com sucesso!")
        return redirect(url_for('upload_page'))
    else:
        # Se a extensão não for permitida
        flash('Tipo de arquivo não permitido. Use PDF, CSV ou OFX.')
        return redirect(url_for('upload_page'))

# --- 5. EXECUÇÃO DA APLICAÇÃO ---

if __name__ == '__main__':
    # debug=True faz o servidor reiniciar automaticamente após cada alteração no código
    app.run(debug=True)
