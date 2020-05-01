import configparser

from potoo import app
from potoo.utils import *


@app.route("/originate/v1")
def originatev1():

    if authorized_ip():

        config = get_config()

        src_context = config['default']['default_originate_context']
        src_exten = config['default']['default_originate_number']
        dest_context = config['default']['default_tennant_context']

        try:   
            dest_exten = get_param('dest_exten')
            dest_context = get_param('dest_context')
            src_exten = get_param('src_exten')
            src_context = get_param('src_context')
        except NameError:
            pass
   
        try:   
            return '<pre>' + run_originate(dest_context,dest_exten,src_context,src_exten) \
                 + '</pre> dest_exten: ' + dest_exten + '<br> dest_context: ' + dest_context \
                 + '<br> src_exten: ' + src_exten + '<br> src_context: ' + src_context
        except NameError:
            return 'all the params are not set'
    
    else:
        return '401'
