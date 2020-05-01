from potoo import app


@app.route("/")
def index():
    return """<h1>Welcome to potoo </h1> <p><a
    href="https://en.wikipedia.org/wiki/Potoo" rel="nofollow">Potoo</a> is a
    special bird that communicates with VoIP ecosystem and particularly well
    with Wazo.</p> <p>The main objective of this project is to quickly (and
    perhaps badly) provide solutions to missing functionalities in a given
    ecosystem.</p> <p>Its best documentation is its source code and Potoo may
    be verry insecure.  </p> """
