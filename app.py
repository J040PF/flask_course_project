from flask import Flask, render_template, request

app = Flask(__name__)
frutas = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('listafrutas'):
            frutas.append(request.form.get('listafrutas'))
    return render_template('index.html', frutas = frutas)


@app.route('/lista', methods=['GET','POST'])
def lista():
    return render_template('lista.html')




if __name__ == "__main__":
    app.run(debug=True)