from potoo import app
from potoo.utils import *

@app.route("/originate/v1")
def originatev1():

    print(authorized_ip())

    dest_context = get_param('dest_context')
    dest_exten = get_param('dest_exten')
    src_exten = get_param('src_exten')
    src_context = get_param('src_context')

    return '<pre>' + run_originate(dest_context,dest_exten,src_context,src_exten) \
         + '</pre> dest_exten: ' + dest_exten + '<br> dest_context: ' + dest_context \
         + '<br> src_exten: ' + src_exten + '<br> src_context: ' + src_context

