##############################################
################ Abjad Tests :) ##############
##############################################

from abjad import *
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def tune():
    duration = Duration(1, 4)
    notes = [Note(pitch, duration) for pitch in range(8)]
    staff = Staff(notes)
    #show(staff)
    systemtools.IOManager.save_last_pdf_as("../resources/tune.pdf")
    return render_template('home.html')

if __name__ == "__main__":
    app.run()

