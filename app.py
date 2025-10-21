from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.sqlite3"
app.secret_key = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)

class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    data_nasc = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(20), nullable=True)
    estado_civil = db.Column(db.String, nullable=True)
    nacionalidade = db.Column(db.String, nullable=True)
    ocupacao = db.Column(db.String, nullable=False)
    telefone_principal = db.Column(db.String, nullable=False)
    telefone_secundario = db.Column(db.String, nullable=True)
    email_principal = db.Column(db.String, nullable=False)
    email_secundario = db.Column(db.String, nullable=True)
    cep = db.Column(db.String, nullable=False)
    logradouro = db.Column(db.String, nullable=False)
    numero_casa = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String, nullable=True)
    bairro = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    pais = db.Column(db.String, nullable=False)

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

@app.route("/", methods=["GET", "POST"])
def principal():
    return render_template("index.html")

@app.route("/visualizar", methods=["GET", "POST"])
def visualizar():
    return render_template("visualizar.html")

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    return render_template("adicionar.html")

@app.route("/excluir", methods=["GET", "POST"])
def excluir():
    return render_template("excluir.html")

@app.route("/editar", methods=["GET", "POST"])
def editar():
    return render_template("editar.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    admin = info.query.filter_by(cpf='00000000000').first()
    if not admin:
        admin = info(
            nome="Administrador",
            cpf="00000000000",
            data_nasc=datetime.strptime("01-01-2000", "%d-%m-%Y").date(),
            genero="Nenhum",
            estado_civil="Nenhum",
            nacionalidade="Nenhuma",
            ocupacao="Administrador",
            telefone_principal="(00) 00000-0000",
            telefone_secundario=None,
            email_principal="Nenhum",
            email_secundario=None,
            cep="00000-000",
            logradouro="Nenhum",
            numero_casa="0",
            complemento=None,
            bairro="Nenhum",
            cidade="Nenhum",
            estado="Nenhum",
            pais="Nenhum"
        )
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True)