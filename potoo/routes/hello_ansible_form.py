import ansible_runner
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from potoo import app
from potoo.utils import *

class helloAnsibleForm(Form):
    sample_var = TextField('Sample var:', validators=[validators.required()])
    
    @app.route("/hello_ansible_form", methods=['GET', 'POST'])
    def hello():
        PLAYBOOK_FILE = os.path.join(os.getcwd(), "potoo/playbooks/hello_ansible_form.yml")
        form = helloAnsibleForm(request.form)
    
        if request.method == 'POST':
            sample_var=request.form['sample_var']
    
        if form.validate():
            extravars = {"sample_var": sample_var}
            r = ansible_runner.run(playbook=PLAYBOOK_FILE, extravars=extravars)
            flash('Sample var: ' + sample_var)
            flash("{}: {}".format(r.status, r.rc))
            flash(r.stats)
        else:
            flash('Error: All the form fields are required.')

        return render_template('hello_ansible_form.html', form=form)
