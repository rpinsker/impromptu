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

# creates lilypond and pdf files but does not display them so that
# later save_last_pdf_as() and save_last_ly_as can be called
def saveLilypondForDisplay(expr, return_timing=False, **kwargs):
    result = abjad.topleveltools.persist(expr).as_pdf(**kwargs)


@app.route('/', methods=['GET', 'POST'])
def tune():
    global tuneObj
    # make a lilypond file, either from tune object previously created or
    # a filler one when page is first loaded
    lilypond_file = makeLilypondFile(tuneObj)
    if request.method == 'POST':
        # change the title. update lilypond file and backend storage of tune object accordingly
        if request.form.has_key('titleInput'):
            title = str(request.form['titleInput'])
            title = title.upper()
            lilypond_file.header_block.title = abjad.markuptools.Markup(title)
            if tuneObj:
                tuneObj.title = title
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        # change the contributors. update lilypond file and backend storage of tune object accordingly
        if request.form.has_key('contributorsInput'):
            composer = str(request.form['contributorsInput'])
            lilypond_file.header_block.composer = abjad.markuptools.Markup(composer)
            if tuneObj:
                tuneObj.contributors = composer
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        # use uploaded file to render a tune object and then render a PDF
        if request.files.has_key('fileInput'):
            file = request.files['fileInput']
            if file and allowed_file(file.filename):
                filename = file.filename  # secure_filename(file.filename)
                file.save(UPLOAD_FOLDER + "/" + filename)
                # call backend to get Tune object
                tune = Tune.Tune.TuneWrapper(UPLOAD_FOLDER + "/" + filename)
                # save it globally to persist when page is reloaded
                tuneObj = tune
                # convert our tune object to notes for abjad and then to a staff
                notes = tuneToNotes(tune)
                staff = abjad.Staff(notes)
                # make lilypond file, setting title and contributors, and then make the PDF
                lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
                lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
                lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
                filenamePDF = updatePDFWithNewLY(lilypond_file)
                return render_template('home.html',filename='static/currentTune/' + filenamePDF + '.pdf')
    # page was loaded normally (not from a request to update name, contributor, or file upload)
    # so display the tune object created at the beginning of the this method
    filenamePDFTemp = updatePDFWithNewLY(lilypond_file)
    return render_template('home.html',filename='static/currentTune/' + filenamePDFTemp + '.pdf')


# convert a Tune object to an array of notes usable by abjad
def tuneToNotes(tune):
    aNotes = []
    for note in tune.notes:
        pitch = note.pitch
        letter = pitch.letter
        accidental = ""
        if pitch.accidental == Tune.Accidental.FLAT:
            accidental += "b"
        elif pitch.accidental == Tune.Accidental.SHARP:
            accidental += "#"
        octave = str(pitch.octave)
        if not letter == "r":
           pitch = abjad.pitchtools.NamedPitch(letter.upper()+accidental+octave)
           if (note.duration):
               duration = abjad.Duration(note.duration[0],note.duration[1])
           else:
               duration = (Tune.Duration.QUARTER[0],Tune.Duration.QUARTER[1])
           aNote = abjad.Note(pitch,duration)
           aNotes.append(aNote)
        else: # handle rests
            if (note.duration):
                duration = str(note.duration[1])
            else:
                duration = "4"
                rest = abjad.scoretools.Rest("r"+duration)
            aNotes.append(rest)
    return aNotes

# makes a lilypond file either from globally stored tune object or makes a filler
# staff and pdf to display when page is first loaded
def makeLilypondFile(tune):
    if tune == None:
        duration = abjad.Duration(1, 4)
        notes = [abjad.Note(pitch, duration) for pitch in range(8)]
        staff = abjad.Staff(notes)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup("SAMPLE TUNE DISPLAY")
        return lilypond_file
    else:
        notes = tuneToNotes(tune)
        staff = abjad.Staff(notes)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
        lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
        return lilypond_file

# lilypond representation has changed so need to prepare to save a new pdf
def updatePDFWithNewLY(lilypond_file):
    saveLilypondForDisplay(lilypond_file)
    # timestamp for pdf name
    filenamePDF = time.strftime("%d%m%Y") + time.strftime("%H%M%S")
    #delete the old file so only one file in currentTune folder at a time
    oldFilenameFile = open("oldFilename.txt", 'r')
    oldFilename = ""
    for line in oldFilenameFile:
        oldFilename = line
    #now write the new file name to oldFilename.txt
    oldFilenameFile = open("oldFilename.txt", 'w')
    oldFilenameFile.write(filenamePDF)
    # save the pdf
    abjad.systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filenamePDF + ".pdf")
    # delete the old file
    subprocess.Popen(["rm", "static/currentTune/" + oldFilename + ".pdf"])
    # return what the pdf is called
    return filenamePDF

if __name__ == "__main__":
    tuneObj = None
    app.debug = True
    app.run(port=1995)

