##############################################
################ Abjad Tests :) ##############
##############################################

import abjad
from flask import render_template, Flask, request, redirect, url_for
from flask import send_from_directory
from flask import Flask
from flask import render_template
#import tuneIvy
#import tuneTest
#import impromptubackendZoe
import Tune

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
    duration = abjad.Duration(1, 4)
    notes = [abjad.Note(pitch, duration) for pitch in range(8)]
    staff = abjad.Staff(notes)
    lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
    if request.method == 'POST':
        if request.form.has_key('titleInput'):
            title = request.form['titleInput']
            title = title.upper()
            lilypond_file.header_block.title = abjad.markuptools.Markup(title)
        if request.form.has_key('contributorsInput'):
            composer = request.form['contributorsInput']
            lilypond_file.header_block.composer = abjad.markuptools.Markup(composer)
        if request.files.has_key('fileInput'):
            file = request.files['fileInput']
            if file and allowed_file(file.filename):
                filename = file.filename  # secure_filename(file.filename)
                print UPLOAD_FOLDER + "/" + filename
                file.save(UPLOAD_FOLDER + "/" + filename)
                #return redirect(url_for('uploaded_file', filename=filename))
    saveLilypondForDisplay(lilypond_file)
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
        if pitch.accidental == Tune.Accidental.FLAT: # changed from impromptubackendZoe.FLAT
            accidental += "f"
        elif pitch.accidental == Tune.Accidental.SHARP: # changed from impromptubackendZoe.SHARP
            accidental += "s"
        octave = str(pitch.octave)
        aNote = abjad.Note(letter+accidental+octave)
        # TODO get actual duration
        aNote.written_duration = abjad.Duration(1,4)
        aNotes.append(aNote)
    return aNotes

if __name__ == "__main__":
    app.debug = True
    app.run(port=1995)

