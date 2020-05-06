import ansible_runner
import os
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField
from potoo import app
from potoo.utils import *


current_smtp_origin = none2null(simple_db_query("SELECT origin FROM mail"))
current_from_email = none2null(simple_db_query("SELECT var_val from staticvoicemail WHERE var_name = 'serveremail'"))
current_from_string = none2null(simple_db_query("SELECT var_val from staticvoicemail WHERE var_name = 'fromstring'"))
current_domain = none2null(simple_db_query("SELECT domain FROM resolvconf"))
current_canonical = none2null(simple_db_query("SELECT canonical FROM mail"))
current_relayhost = none2null(simple_db_query("SELECT relayhost FROM mail"))
current_fallback_relayhost = none2null(simple_db_query("SELECT fallback_relayhost FROM mail"))
current_hostname = none2null(simple_db_query("SELECT hostname FROM resolvconf"))
current_mail_domain = none2null(simple_db_query("SELECT mydomain FROM mail"))
current_nameserver1 = none2null(simple_db_query("SELECT nameserver1 FROM resolvconf"))
current_nameserver2 = none2null(simple_db_query("SELECT nameserver2 FROM resolvconf"))
current_nameserver3 = none2null(simple_db_query("SELECT nameserver3 FROM resolvconf"))
current_voip_iface = none2null(simple_db_query("SELECT ifname FROM netiface WHERE networktype='voip'"))
current_voip_address = none2null(simple_db_query("SELECT address FROM netiface"))


class update_system_info_form(Form):
    smtp_origin = TextField('smtp_origin: ', validators=[validators.required()],
            description="domain.tld", default=current_smtp_origin )
    from_email = TextField('from_email: ', validators=[validators.required()],
            description="no-reply@domain.tld", default=current_from_email )
    from_string = TextField('from_string: ', validators=[validators.required()],
            description="Wazo PBX", default=current_from_string )
    domain = TextField('domain:', validators=[validators.required()],
            description="domain.tld", default=current_domain )
    canonical = TextField('canonical: ', validators=[validators.required()],
            description="asterisk no-reply@domain.tld\\nroot no-reply@domain.tld", default=current_canonical )
    relayhost = TextField('relayhost: ', validators=[validators.required()],
            description="smtp.domain.tld ( null = none )", default=current_relayhost )
    fallback_relayhost = TextField('fallback_relayhost: ', validators=[validators.required()],
            description="smtp2.domain.tld ( null = none )", default=current_fallback_relayhost )
    hostname = TextField('hostname:',
            validators=[validators.required()], description="my-machine", default=current_hostname )
    mail_domain = TextField('mail_domain:', validators=[validators.required()],
            description="domain.tld", default=current_mail_domain )
    nameserver1 = TextField('nameserver1: ', validators=[validators.required()],
            description="192.168.0.254", default=current_nameserver1 )
    nameserver2 = TextField('nameserver2: ', validators=[validators.required()],
            description="192.168.0.253 ( null = none )", default=current_nameserver2 )
    nameserver3 = TextField('nameserver3: ', validators=[validators.required()],
             description="192.168.0.252 ( null = none )", default=current_nameserver3 )
    voip_iface = TextField('voip_iface: ', validators=[validators.required()],
            description="ens224", default=current_voip_iface )
    voip_address = TextField('voip_address: ', validators=[validators.required()],
            description="192.168.0.250", default=current_voip_address )
    apply_config = BooleanField('Apply' )
    
    @app.route("/update_system_info", methods=['GET', 'POST'])
    def update_system_info():
        PLAYBOOK_FILE = os.path.join(os.getcwd(), "potoo/playbooks/update-system-info.yml")
        form = update_system_info_form(request.form)
    
        if request.method == 'POST':
            extravars = request.form.to_dict()
            for item, value in extravars.items():
                if value == 'null':
                    extravars[item] = ''
    
        if form.validate() and request.method == 'POST':
            r = ansible_runner.run(playbook=PLAYBOOK_FILE, extravars=extravars)
            flash('extravars: ' + str(extravars))
            flash("{}: {}".format(r.status, r.rc))
            flash(r.stats)
        else:
            flash('All the form fields are required.')


        return render_template('update_system_info.html', form=form)
