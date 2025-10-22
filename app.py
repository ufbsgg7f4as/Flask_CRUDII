from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)

class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    data_nasc = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(20), nullable=True)
    estado_civil = db.Column(db.String(30), nullable=True)
    nacionalidade = db.Column(db.String(50), nullable=True)
    ocupacao = db.Column(db.String(50), nullable=False)
    telefone_principal = db.Column(db.String(20), nullable=False)
    telefone_secundario = db.Column(db.String(20), nullable=True)
    email_principal = db.Column(db.String(100), nullable=False)
    email_secundario = db.Column(db.String(100), nullable=True)
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    numero_casa = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(50), nullable=True)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    pais = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, cpf, data_nasc, genero, estado_civil, nacionalidade,
                 ocupacao, telefone_principal, telefone_secundario, email_principal,
                 email_secundario, cep, logradouro, numero_casa, complemento,
                 bairro, cidade, estado, pais):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.genero = genero
        self.estado_civil = estado_civil
        self.nacionalidade = nacionalidade
        self.ocupacao = ocupacao
        self.telefone_principal = telefone_principal
        self.telefone_secundario = telefone_secundario
        self.email_principal = email_principal
        self.email_secundario = email_secundario
        self.cep = cep
        self.logradouro = logradouro
        self.numero_casa = numero_casa
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais

    def __repr__(self):
        return f'<Cliente {self.nome}>'

# ========== ROTAS ==========

@app.route("/")
def principal():
    """Página inicial - redireciona para visualizar"""
    return redirect(url_for('visualizar'))

@app.route("/visualizar")
def visualizar():
    """Página para visualizar todos os clientes"""
    clientes = info.query.all()
    
    # Estatísticas para o template
    cidades = list(set([cliente.cidade for cliente in clientes if cliente.cidade]))
    estados = list(set([cliente.estado for cliente in clientes if cliente.estado]))
    ocupacoes = list(set([cliente.ocupacao for cliente in clientes if cliente.ocupacao]))
    
    return render_template("visualizar.html", 
                         clientes=clientes,
                         cidades=sorted(cidades),
                         estados=sorted(estados),
                         ocupacoes=sorted(ocupacoes))

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    """Página para adicionar novo cliente"""
    if request.method == "POST":
        try:
            # Validar CPF único
            cpf_existente = info.query.filter_by(cpf=request.form['cpf']).first()
            if cpf_existente:
                flash('CPF já cadastrado no sistema!', 'error')
                return render_template("adicionar.html")
            
            # Converter data
            data_nasc = datetime.strptime(request.form['data_nasc'], '%Y-%m-%d').date()
            
            # Criar novo cliente
            novo_cliente = info(
                nome=request.form['nome'].strip(),
                cpf=request.form['cpf'].strip(),
                data_nasc=data_nasc,
                genero=request.form.get('genero'),
                estado_civil=request.form.get('estado_civil'),
                nacionalidade=request.form.get('nacionalidade'),
                ocupacao=request.form['ocupacao'].strip(),
                telefone_principal=request.form['telefone_principal'].strip(),
                telefone_secundario=request.form.get('telefone_secundario', '').strip() or None,
                email_principal=request.form['email_principal'].strip(),
                email_secundario=request.form.get('email_secundario', '').strip() or None,
                cep=request.form['cep'].strip(),
                logradouro=request.form['logradouro'].strip(),
                numero_casa=request.form['numero_casa'].strip(),
                complemento=request.form.get('complemento', '').strip() or None,
                bairro=request.form['bairro'].strip(),
                cidade=request.form['cidade'].strip(),
                estado=request.form['estado'].strip(),
                pais=request.form.get('pais', 'Brasil').strip()
            )
            
            db.session.add(novo_cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('visualizar'))
            
        except ValueError as e:
            flash('Erro na formatação da data de nascimento!', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {str(e)}', 'error')
    
    return render_template("adicionar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """Página para editar cliente existente"""
    cliente = info.query.get_or_404(id)
    
    if request.method == "POST":
        try:
            # Converter data
            data_nasc = datetime.strptime(request.form['data_nasc'], '%Y-%m-%d').date()
            
            # Atualizar dados do cliente
            cliente.nome = request.form['nome'].strip()
            cliente.data_nasc = data_nasc
            cliente.genero = request.form.get('genero')
            cliente.estado_civil = request.form.get('estado_civil')
            cliente.nacionalidade = request.form.get('nacionalidade')
            cliente.ocupacao = request.form['ocupacao'].strip()
            cliente.telefone_principal = request.form['telefone_principal'].strip()
            cliente.telefone_secundario = request.form.get('telefone_secundario', '').strip() or None
            cliente.email_principal = request.form['email_principal'].strip()
            cliente.email_secundario = request.form.get('email_secundario', '').strip() or None
            cliente.cep = request.form['cep'].strip()
            cliente.logradouro = request.form['logradouro'].strip()
            cliente.numero_casa = request.form['numero_casa'].strip()
            cliente.complemento = request.form.get('complemento', '').strip() or None
            cliente.bairro = request.form['bairro'].strip()
            cliente.cidade = request.form['cidade'].strip()
            cliente.estado = request.form['estado'].strip()
            cliente.pais = request.form.get('pais', 'Brasil').strip()
            
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('visualizar'))
            
        except ValueError as e:
            flash('Erro na formatação da data de nascimento!', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {str(e)}', 'error')
    
    return render_template("editar.html", cliente=cliente)

@app.route("/excluir/<int:id>")
def excluir(id):
    """Rota para excluir cliente"""
    cliente = info.query.get_or_404(id)
    nome_cliente = cliente.nome
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente "{nome_cliente}" excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cliente: {str(e)}', 'error')
    
    return redirect(url_for('visualizar'))

# ========== FILTROS PERSONALIZADOS ==========

@app.template_filter('format_cpf')
def format_cpf(cpf):
    """Filtro para formatar CPF"""
    if cpf and len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

@app.template_filter('format_telefone')
def format_telefone(telefone):
    """Filtro para formatar telefone"""
    if telefone:
        # Remove caracteres não numéricos
        nums = ''.join(filter(str.isdigit, telefone))
        if len(nums) == 11:
            return f"({nums[:2]}) {nums[2:7]}-{nums[7:]}"
        elif len(nums) == 10:
            return f"({nums[:2]}) {nums[2:6]}-{nums[6:]}"
    return telefone

# ========== INICIALIZAÇÃO ==========

def criar_admin():
    """Função para criar usuário admin padrão"""
    admin = info.query.filter_by(cpf='00000000000').first()
    if not admin:
        try:
            admin = info(
                nome="Administrador do Sistema",
                cpf="00000000000",
                data_nasc=datetime.strptime("2000-01-01", "%Y-%m-%d").date(),
                genero="Prefiro não informar",
                estado_civil="Solteiro(a)",
                nacionalidade="Brasileira",
                ocupacao="Administrador",
                telefone_principal="(00) 00000-0000",
                telefone_secundario=None,
                email_principal="admin@sistema.com",
                email_secundario=None,
                cep="00000-000",
                logradouro="Endereço administrativo",
                numero_casa="S/N",
                complemento=None,
                bairro="Centro",
                cidade="São Paulo",
                estado="SP",
                pais="Brasil"
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar admin: {e}")

# ========== EXECUÇÃO ==========

if __name__ == "__main__":
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Criar admin padrão
        criar_admin()
        
        # Verificar se há clientes
        total_clientes = info.query.count()
        print(f"📊 Total de clientes no banco: {total_clientes}")
    
    # Executar aplicação
    app.run(debug=True, host='0.0.0.0', port=5000)