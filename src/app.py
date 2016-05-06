##############################################
################ Abjad Tests :) ##############
##############################################

from abjad import *
from flask import Flask
app = Flask(__name__)

@app.route("/")
def tune():
    duration = Duration(1, 4)
    notes = [Note(pitch, duration) for pitch in range(8)]
    staff = Staff(notes)
    #show(staff)
    systemtools.IOManager.save_last_pdf_as("../resources/tune.pdf")
    return "hello"

if __name__ == "__main__":
    tune()
    app.run()

