from flask import Flask, render_template, request

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




if __name__ == "__main__":
    app.run(debug=True)