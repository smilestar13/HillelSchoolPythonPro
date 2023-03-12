from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return 'Hello :)'


@app.route("/registration", methods=['GET', 'POST'])
def registration(*args, **kwargs):
    context = {}

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        with open('user_data.log', 'r') as work_one:
            for el in work_one:
                separator = el.find('- PASS -')
                if f" '{name}' " in el[:separator]:
                    return redirect(url_for('login'))

        with open('user_data.log', 'a') as work_one:
            work_one.write(f"- NAME - > '{name}' - PASS - > '{password}'\n")
            context.update({'result': f'Dear, {name}: congratulations on your registration!'})

    return render_template('registration.html', **context)


@app.route("/login", methods=['GET', 'POST'])
def login(*args, **kwargs):
    context = {}

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        with open('user_data.log', 'r') as work_one:
            for el in work_one:
                separator = el.find('- PASS -')
                if f" '{name}' " in el[:separator] and f" '{password}'" in el[separator:]:
                    context.update({'result': f'Dear, {name}: You are in a system!'})
                    return render_template('login.html', **context)
                else:
                    context.update({'result': f'Invalid user data!!! Try again...'})

    return render_template('login.html', **context)
