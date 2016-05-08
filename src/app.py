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
    print "HI"
    result = topleveltools.persist(expr).as_pdf(**kwargs)
    pdf_file_path = result[0]
    print pdf_file_path
    abjad_formatting_time = result[1]
    lilypond_rendering_time = result[2]
    success = result[3]

@app.route("/")
def tune():
    duration = Duration(1, 8)
    notes = [Note(pitch, duration) for pitch in range(8)]
    staff = Staff(notes)
    saveLilypondForDisplay(staff)
    #score = Score([staff])
    #lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    #lilypond_file.layout_block.indent = 0
    #lilypond_file.paper_block.top_margin = 15
    #lilypond_file.paper_block.left_margin = 15
    #lilypondStr = str(format(lilypond_file))
    #f = open('simple.ly','w')
    #f.write(lilypondStr)

    #show(staff)
    # systemtools.IOManager.save_last_pdf_as("static/tune.pdf")
    #subprocess.call('rm static/currentTune/*.pdf')
    #subprocess.Popen(["lilypond","simple.ly","&&","mv","simple.pdf","static/tune.pdf"])
    filename = time.strftime("%d:%m:%Y") + time.strftime("%H:%M:%S")
    #subprocess.call('lilypond --output=static/currentTune/' + filename simple.ly',shell=True) #
    print "hello"

    #systemtools.IOManager.save_last_ly_as(filename + ".ly")
    systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filename + ".pdf")
    return render_template('home.html',filename='static/currentTune/' + filename + '.pdf')

if __name__ == "__main__":
    app.run()

