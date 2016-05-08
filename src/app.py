##############################################
################ Abjad Tests :) ##############
##############################################

from abjad import *
from flask import Flask
from flask import render_template

import subprocess
import time
app = Flask(__name__)

def saveLilypondForDisplay(expr, return_timing=False, **kwargs):
    result = topleveltools.persist(expr).as_pdf(**kwargs)
    pdf_file_path = result[0]
    abjad_formatting_time = result[1]
    lilypond_rendering_time = result[2]
    success = result[3]

@app.route("/")
def tune():
    duration = Duration(1, 4)
    notes = [Note(pitch, duration) for pitch in range(8)]
    staff = Staff(notes)
    saveLilypondForDisplay(staff)

    filename = time.strftime("%d%m%Y") + time.strftime("%H%M%S")


    oldFilenameFile = open("oldFilename.txt",'r')
    oldFilename = ""
    for line in oldFilenameFile:
        oldFilename = line

    oldFilenameFile = open("oldFilename.txt", 'w')
    oldFilenameFile.write(filename)

    systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filename + ".pdf")

    subprocess.Popen(["rm","static/currentTune/"+oldFilename+".pdf"])

    return render_template('home.html',filename='static/currentTune/' + filename + '.pdf')

if __name__ == "__main__":
    app.run(port=1995)

