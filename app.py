from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import urllib.request, json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
app.app_context().push()

db = SQLAlchemy(app)

frutas = ["banana", "maça", "pera"]
registros = [{"nome":"joao", "nota":10}, {"nome":"maria", "nota":8}]


# ---------- criar banco de dados
class cursos(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch
# ---------- Fim criar banco de dados


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        if request.form.get('listafrutas'):
            frutas.append(request.form.get('listafrutas'))
    return render_template('index.html', frutas = frutas)


@app.route('/sobre', methods=['GET','POST'])
def sobre():
    if request.method == "POST" and request.form.get('nome') and request.form.get('nota'):
        registros.append({"nome":request.form.get('nome'), "nota":request.form.get('nota')})

    return render_template('lista.html', registros = registros)


@app.route('/filmes')
def filmes():
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=1210749afa33db66c07848d986de0fa4'
    resposta = urllib.request.urlopen(url)
    dados = json.loads(resposta.read())

    
    return render_template('filmes.html', dados= dados['results'])



#  -------------------- criar, atualizar e deletar o banco de dados
@app.route('/curso')
def curso():
    return render_template('cursos.html', cursos = cursos.query.all())


@app.route('/adicionar-novo-curso', methods=["GET","POST"])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('carga-horaria')

    if request.method == 'POST':
        curso = cursos(nome, descricao, ch)
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('curso'))

    return render_template('cria-curso.html')


@app.route('/<int:id>/atualiza_curso', methods = ['GET','POST'])
def atualiza_curso(id):
    curso = cursos.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        ch = request.form['carga-horaria']

        cursos.query.filter_by(id=id).update({'nome':nome, 'descricao':descricao, 'ch':ch})
        db.session.commit()

        return redirect(url_for('curso'))


    return render_template('atualiza_curso.html', curso = curso)

@app.route('/<int:id>/remover_curso')
def remover_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('curso'))


#  -------------------- Fim criar, atualizar e deletar o banco de dados



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)