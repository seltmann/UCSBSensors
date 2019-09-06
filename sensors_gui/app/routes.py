from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/csv', methods=['GET', 'POST'])
def index():
    form = CSV(request.form)
    if request.method == 'POST' and form.validate():
        result = (form.d.data, form.t.data, form.w.data)
        o1 = request.form.getlist('o1')
        o2 = request.form.getlist('o2')
        o3 = request.form.getlist('o3')
        o4 = request.form.getlist('o4')
        o5 = request.form.getlist('o5')
        o6 = request.form.getlist('o6')
        o7 = request.form.getlist('o7')
        o8 = request.form.getlist('o8')
        o9 = request.form.getlist('o9')
        o10 = request.form.getlist('o10')
        o11 = request.form.getlist('o11')
        o12 = request.form.getlist('o12')
    else:
        result = None

    return render_template('csv.html', title='Make CSV File', :wq
            form=form, result=result)
