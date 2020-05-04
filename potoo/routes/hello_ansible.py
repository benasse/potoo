import ansible_runner
from potoo import app
from potoo.utils import *

@app.route("/hello_ansible")
def hello_ansible():

    PLAYBOOK_FILE = os.path.join(os.getcwd(), "potoo/playbooks/hello_ansible.yml")

    r = ansible_runner.run(playbook=PLAYBOOK_FILE, extravars={"my_var":"content"})

    return r.stats
