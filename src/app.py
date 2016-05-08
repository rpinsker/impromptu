##############################################
################ Abjad Tests :) ##############
##############################################

import abjad
from flask import render_template, Flask, request, redirect, url_for
from flask import send_from_directory
from flask import Flask
from flask import render_template
import tuneIvy
import tuneTest
import impromptubackendZoe

import subprocess
import time
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['mid', 'midi'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def saveLilypondForDisplay(expr, return_timing=False, **kwargs):
    result = abjad.topleveltools.persist(expr).as_pdf(**kwargs)
    pdf_file_path = result[0]
    abjad_formatting_time = result[1]
    lilypond_rendering_time = result[2]
    success = result[3]

@app.route('/', methods=['GET', 'POST'])
def tune():
    if request.method == 'POST':
        file = request.files['fileInput']
        if file and allowed_file(file.filename):
            filename = file.filename #secure_filename(file.filename)
            print UPLOAD_FOLDER + "/" + filename
            file.save(UPLOAD_FOLDER + "/" + filename)
            #return redirect(url_for('uploaded_file', filename=filename))
    duration = abjad.Duration(1, 4)
    notes = [abjad.Note(pitch, duration) for pitch in range(8)]
    note = Note("cs8")
    note.written_duration = Duration(1,1)
    notes.append(note)
    # TODO USE THIS ONCE ACTUAL TUNE IS BEING GENERATED ON OUR BACKEND
    # tune = tuneTest.Tune()
    # notes = tuneToNotes(tune)
    staff = abjad.Staff(notes)
    saveLilypondForDisplay(staff)

    filename = time.strftime("%d%m%Y") + time.strftime("%H%M%S")

    oldFilenameFile = open("oldFilename.txt",'r')
    oldFilename = ""
    for line in oldFilenameFile:
        oldFilename = line
    oldFilenameFile = open("oldFilename.txt", 'w')
    oldFilenameFile.write(filename)
    abjad.systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filename + ".pdf")
    subprocess.Popen(["rm","static/currentTune/"+oldFilename+".pdf"])
    return render_template('home.html',filename='static/currentTune/' + filename + '.pdf')


def tuneToNotes(tune):
    aNotes = []
    for note in tune.notes:
        # if not note.isRest():
        pitch = note.pitch
        letter = pitch.letter
        accidental = ""
        if pitch.accidental == impromptubackendZoe.FLAT:
            accidental += "f"
        elif pitch.accidental == impromptubackendZoe.SHARP:
            accidental += "s"
        octave = str(pitch.octave)
        aNote = abjad.Note(letter+accidental+octave)
        # TODO get actual duration
        aNote.written_duration = abjad.Duration(1,4)
        aNotes.append(aNote)
    return aNotes

if __name__ == "__main__":
    app.run(port=1995)

