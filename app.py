from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)
frutas = ["banana", "maça", "pera"]
registros = [{"nome":"joao", "nota":10}, {"nome":"maria", "nota":8}]


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



if __name__ == "__main__":
    app.run(debug=True)