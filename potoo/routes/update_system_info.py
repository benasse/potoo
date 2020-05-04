import ansible_runner
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from potoo import app
from potoo.utils import *

class update_system_info_form(Form):
    smtp_origin = TextField('smtp_origin: ', validators=[validators.required()],
            description="no-reply@domain.tld" )
    from_string = TextField('from_string: ', validators=[validators.required()],
            description="Wazo PBX" )
    domain = TextField('domain:', validators=[validators.required()],
            description="domain.tld" )
    canonical = TextField('canonical: ', validators=[validators.required()],
            description="asterisk no-reply@domain.tld\\n+root no-reply@domain.tld" )
    relayhost = TextField('relayhost: ', validators=[validators.required()],
            description="smtp.domain.tld ( '' = none )" )
    fallback_relayhost = TextField('fallback_relayhost: ', validators=[validators.required()],
            description="smtp2.domain.tld ( '' = none )" )
    hostname = TextField('hostname:',
            validators=[validators.required()], description="my-machine" )
    mail_domain = TextField('mail_domain:', validators=[validators.required()],
            description="domain.tld" )                                   
    nameserver1 = TextField('nameserver1: ', validators=[validators.required()],
            description="192.168.0.254" )
    nameserver2 = TextField('nameserver2: ', validators=[validators.required()],
            description="192.168.0.253 ( '' = none )" )
    nameserver3 = TextField('nameserver3: ', validators=[validators.required()],
             description="192.168.0.252 ( '' = none )" )
    voip_iface = TextField('voip_iface: ', validators=[validators.required()],
            description="ens224" )
    voip_address = TextField('voip_address: ', validators=[validators.required()],
            description="192.168.0.250" )
    
    @app.route("/update_system_info", methods=['GET', 'POST'])
    def update_system_info():
        PLAYBOOK_FILE = os.path.join(os.getcwd(), "potoo/playbooks/hello_ansible_form.yml")
        form = update_system_info_form(request.form)
    
        if request.method == 'POST':
            smtp_origin=request.form['smtp_origin']
    
        if form.validate():
            extravars = {"sample_var": smtp_origin}
            r = ansible_runner.run(playbook=PLAYBOOK_FILE, extravars=extravars)
            flash('Sample var: ' + smtp_origin)
            flash("{}: {}".format(r.status, r.rc))
            flash(r.stats)
        else:
            flash('All the form fields are required.')

        return render_template('update_system_info.html', form=form)
