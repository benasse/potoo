from potoo import app

@app.route("/")
def index():
        return """
        <h1>Welcome to potoo </h1>
        Potoo is a special bird that communicates with VoIP ecosystem and particularly well with Wazo
        """
