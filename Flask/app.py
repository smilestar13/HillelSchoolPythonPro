from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return 'Hello user!'


@app.route("/registration", methods=['GET', 'POST'])
def registration(*args, **kwargs):
    context = {}
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        context.update({'name': name, 'password': password})
        return render_template('index.html', **context)
