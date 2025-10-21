from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração do banco de dados
DATABASE = 'funcionarios.db'

def init_db():
    """Inicializa o banco de dados com a tabela de funcionários"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            anos_empresa INTEGER NOT NULL,
            anos_experiencia INTEGER NOT NULL,
            funcao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Cria uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Página inicial - Lista todos os funcionários"""
    conn = get_db_connection()
    funcionarios = conn.execute('SELECT * FROM funcionarios').fetchall()
    conn.close()
    return render_template('index.html', funcionarios=funcionarios)

@app.route('/cadastrar', methods=('GET', 'POST'))
def cadastrar_funcionario():
    """Cadastra um novo funcionário"""
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        anos_empresa = request.form['anos_empresa']
        anos_experiencia = request.form['anos_experiencia']
        funcao = request.form['funcao']
        
        if not nome or not idade or not anos_empresa or not anos_experiencia or not funcao:
            flash('Todos os campos são obrigatórios!')
        else:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO funcionarios (nome, idade, anos_empresa, anos_experiencia, funcao)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, idade, anos_empresa, anos_experiencia, funcao))
            conn.commit()
            conn.close()
            flash('Funcionário cadastrado com sucesso!')
            return redirect(url_for('index'))
    
    return render_template('cadastrar.html')

@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar_funcionario(id):
    """Edita um funcionário existente"""
    conn = get_db_connection()
    funcionario = conn.execute('SELECT * FROM funcionarios WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        anos_empresa = request.form['anos_empresa']
        anos_experiencia = request.form['anos_experiencia']
        funcao = request.form['funcao']
        
        if not nome or not idade or not anos_empresa or not anos_experiencia or not funcao:
            flash('Todos os campos são obrigatórios!')
        else:
            conn.execute('''
                UPDATE funcionarios 
                SET nome = ?, idade = ?, anos_empresa = ?, anos_experiencia = ?, funcao = ?
                WHERE id = ?
            ''', (nome, idade, anos_empresa, anos_experiencia, funcao, id))
            conn.commit()
            conn.close()
            flash('Funcionário atualizado com sucesso!')
            return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar.html', funcionario=funcionario)

@app.route('/excluir/<int:id>')
def excluir_funcionario(id):
    """Exclui um funcionário"""
    conn = get_db_connection()
    conn.execute('DELETE FROM funcionarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Funcionário excluído com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)