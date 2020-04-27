from ansi2html import Ansi2HTMLConverter
from potoo import app
from potoo.utils import *


@app.route("/queue")
def queue_show():

    if authorized_ip():
        queue = ''
        try:
            queue = get_param('queue')
        except:
            pass
    
        cmd = '/usr/sbin/rasterisk -rx "queue show ' + queue + '"'
    
        stdout = run_shell(cmd)
        html = stdout2html(stdout)

        return html
    else:
        return '401'


@app.route("/queue_pretty")
def queue_show_pretty():

    if authorized_ip():
        queue = ''
        try:
            queue = get_param('queue')
        except:
            pass
    
        cmd = '/usr/sbin/rasterisk -rx "queue show ' + queue + '" | awk -F"(" \'{print $1$5$6}\' '
    
        stdout = run_shell(cmd)
        html = stdout2html(stdout)

        return html

    else:
        return '401'
