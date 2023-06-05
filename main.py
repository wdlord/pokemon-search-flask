from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import CSRFProtect
from pokemon import get_pokemon
import random


app = Flask(__name__)

# created with secrets.token_hex(16) in separate python console.
app.config['SECRET_KEY'] = 'b041becfa469cd0787dc7e1cd168d313'

# Flask-WTF requires this line
csrf = CSRFProtect(app)


@app.route("/", methods=['GET', 'POST'])
def home():

    # This handles either of the two form buttons being pressed.
    if request.method == 'POST':

        # This indicates that the user searched a specific Pokémon.
        if request.form.get('submit'):
            pokemon = get_pokemon(request.form['name'].strip().lower())

        # This indicates the user requested a random Pokémon.
        elif request.form.get('random'):
            pokemon = get_pokemon()

    # This handles loading the page if neither button was clicked.
    else:
        pokemon = get_pokemon()

    return render_template("home.html", pokemon=pokemon)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))
