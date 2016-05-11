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

tuneObj = None

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
    global tuneObj
    if tuneObj == None:
        duration = abjad.Duration(1, 4)
        notes = [abjad.Note(pitch, duration) for pitch in range(8)]
        staff = abjad.Staff(notes)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup("SAMPLE TUNE DISPLAY")
    else:
        notes = tuneToNotes(tuneObj)
        staff = abjad.Staff(notes)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup(tuneObj.title)
        lilypond_file.header_block.composer = abjad.markuptools.Markup(tuneObj.contributors)

    if request.method == 'POST':
        if request.form.has_key('titleInput'):
            title = request.form['titleInput']
            title = title.upper()
            lilypond_file.header_block.title = abjad.markuptools.Markup(str(title))
            if tuneObj:
                tuneObj.title = title
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        if request.form.has_key('contributorsInput'):
            composer = request.form['contributorsInput']
            lilypond_file.header_block.composer = abjad.markuptools.Markup(str(composer))
            if tuneObj:
                tuneObj.contributors = composer
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        if request.files.has_key('fileInput'):
            file = request.files['fileInput']
            if file and allowed_file(file.filename):
                filename = file.filename  # secure_filename(file.filename)
                print UPLOAD_FOLDER + "/" + filename
                file.save(UPLOAD_FOLDER + "/" + filename)
                #return redirect(url_for('uploaded_file', filename=filename))
                tune = Tune.Tune.TuneWrapper(UPLOAD_FOLDER + "/" + filename)
                tuneObj = tune
                notes = tuneToNotes(tune)
                staff = abjad.Staff(notes)
                lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
                lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
                lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
                filenamePDF = updatePDFWithNewLY(lilypond_file)
                return render_template('home.html',filename='static/currentTune/' + filenamePDF + '.pdf')
    #abjad.systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filenamePDFTemp + ".pdf")
    filenamePDFTemp = updatePDFWithNewLY(lilypond_file)
    return render_template('home.html',filename='static/currentTune/' + filenamePDFTemp + '.pdf')

def tuneToNotes(tune):
    aNotes = []
    for note in tune.notes:
        # if not note.isRest():
        pitch = note.pitch
        letter = pitch.letter
        accidental = ""
        if pitch.accidental == Tune.Accidental.FLAT: # changed from impromptubackendZoe.FLAT
            accidental += "b"
        elif pitch.accidental == Tune.Accidental.SHARP: # changed from impromptubackendZoe.SHARP
            accidental += "#"
        octave = str(pitch.octave)
        if not letter == "r":
           pitch = abjad.pitchtools.NamedPitch(letter.upper()+accidental+octave)
           aNote = abjad.Note(pitch,abjad.Duration(note.duration[0],note.duration[1]))
           aNotes.append(aNote)
        else:
            rest = abjad.scoretools.Rest("r"+str(note.duration[1]))
            aNotes.append(rest)
    return aNotes


def updatePDFWithNewLY(lilypond_file):
    saveLilypondForDisplay(lilypond_file)
    filenamePDF = time.strftime("%d%m%Y") + time.strftime("%H%M%S")
    oldFilenameFile = open("oldFilename.txt", 'r')
    oldFilename = ""
    for line in oldFilenameFile:
        oldFilename = line
    oldFilenameFile = open("oldFilename.txt", 'w')
    oldFilenameFile.write(filenamePDF)
    abjad.systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filenamePDF + ".pdf")
    subprocess.Popen(["rm", "static/currentTune/" + oldFilename + ".pdf"])
    return filenamePDF

if __name__ == "__main__":
    tuneObj = None
    app.debug = True
    app.run(port=1995)

