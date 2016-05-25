
import abjad
from flask import render_template, Flask, request, redirect, url_for
from flask import send_from_directory
from flask import Flask
from flask import render_template
import Tune #TuneIter2 as Tune
import glob

import os, subprocess
import time
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['mid', 'midi', 'mp3', 'wav','json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tuneObj = None
measuresObj = None

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

def save_measure_as_png(expr, i, return_timing=False, **kwargs):
    if i == 0:
        subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.png"))
        subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.ly"))
    # SAVE AS A PNG
    result = abjad.topleveltools.persist(expr).as_png('static/currentTune/'+ str(i) + '.png',**kwargs)


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
            if validTitleOrNames(title):
                title = title.upper()
                lilypond_file.header_block.title = abjad.markuptools.Markup(title)
                if tuneObj:
                    tuneObj.title = title
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        # change the contributors. update lilypond file and backend storage of tune object accordingly
        if request.form.has_key('contributorsInput'):
            composer = str(request.form['contributorsInput'])
            if validTitleOrNames(composer):
                lilypond_file.header_block.composer = abjad.markuptools.Markup(composer)
                if tuneObj:
                    tuneObj.contributors = composer
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        # use uploaded file to render a tune object and then render a PDF
        if request.files.has_key('fileInput'):
            file = request.files['fileInput']
            if file and allowed_file(file.filename):
                filename = os.path.basename(file.filename)  # secure_filename(file.filename)
                file.save(UPLOAD_FOLDER + "/" + filename)
                # call backend to get Tune object
                tune = Tune.Tune.TuneWrapper(UPLOAD_FOLDER + "/" + filename)
                # save it globally to persist when page is reloaded
                tuneObj = tune
                # convert our tune object to notes for abjad and then to a staff
                staff = makeStaffFromTune(tune) #abjad.Staff(notes)
                # make lilypond file, setting title and contributors, and then make the PDF
                lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
                lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
                lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
                filenamePDF = updatePDFWithNewLY(lilypond_file)

                listOfMeasures = tunetoMeasures(tuneObj)
                listOfPNGs = []
                for m in range(len(listOfMeasures)):
                    name = "static/currentTune/" + str(m+1) + ".png"
                    listOfPNGs.append(name)
                return render_template('home.html',filename='static/currentTune/' + filenamePDF + '.pdf', measures=listOfMeasures, measureImgs=listOfPNGs)

        if request.files.has_key('jsonInput'):
            file = request.files['jsonInput']
            if file and allowed_file(file.filename):
                filename = os.path.basename(file.filename)  # secure_filename(file.filename)
                file.save(UPLOAD_FOLDER + "/" + filename)
                # call backend to get Tune object
                tune = Tune.Tune.TuneWrapper(UPLOAD_FOLDER + "/" + filename)
                # save it globally to persist when page is reloaded
                tuneObj = tune
                # convert our tune object to notes for abjad and then to a staff
                staff = makeStaffFromTune(tune)  # abjad.Staff(notes)
                # make lilypond file, setting title and contributors, and then make the PDF
                lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
                lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
                lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
                filenamePDF = updatePDFWithNewLY(lilypond_file)
                return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')

    # page was loaded normally (not from a request to update name, contributor, or file upload)

    # so display the tune object created at the beginning of the this method
    filenamePDFTemp = updatePDFWithNewLY(lilypond_file)
    return render_template('home.html',filename='static/currentTune/' + filenamePDFTemp + '.pdf')


def measureIndexToPNGFilepath(i):
    if i < len(measuresObj) and i >= 0:
        m = measuresObj[i]
        return save_measure_as_png(m,i)
    else:
        "bad index!"


# convert a Tune object to an array of notes usable by abjad
def tuneToNotes(tune):
    if tune == None:
        return []

    listOfMeasures = tunetoMeasures(tune)

    aNotes = [] # holds lists of notes corresponding to measures

    for measure in listOfMeasures:
        currentMeasure = []
        for event in measure:# changed tuneiter2
            aChord = None
            pitches = event.getPitch()
            if pitches == None:
                pitches = []
            pitches = [p for p in pitches if p is not None]
            for pitch in pitches:
                letter = pitch.letter
                accidental = ""
                if pitch.accidental == Tune.Accidental.FLAT:
                    accidental += "b"
                elif pitch.accidental == Tune.Accidental.SHARP:
                    accidental += "#"
                octave = str(pitch.octave)
                if letter:
                    if not letter == "r":
                       if not aChord:
                           aChord = abjad.Chord([],abjad.Duration(Tune.Duration.QUARTER[0],Tune.Duration.QUARTER[1]))
                       pitch = abjad.pitchtools.NamedPitch(letter.upper()+accidental+octave)
                       if (event.duration):
                           duration = abjad.Duration(event.duration[0],event.duration[1])
                       else:
                           duration = abjad.Duration(Tune.Duration.QUARTER[0],Tune.Duration.QUARTER[1])
                       aChord.written_duration = duration
                       aChord.note_heads.append(abjad.pitchtools.NamedPitch(letter.upper() + accidental + octave))
                       #aNote = abjad.Note(pitch,duration)
                       #aNotes.append(aNote)
                    else: # handle rests
                        if (event.duration):
                            duration = str(int(event.duration[1]))
                        else:
                            duration = "4"
                        rest = abjad.scoretools.Rest("r"+duration)
                        currentMeasure.append(rest)

            if (aChord): # only set if this is a note or a chord
                currentMeasure.append(aChord)
        if (len(currentMeasure) > 0):
            aNotes.append(currentMeasure)
    return aNotes


def tunetoMeasures(tune):
    if tune == None:
        return []
    measures = []
    measureTime = float(tune.getTimeSignature()[0]) / float(tune.getTimeSignature()[1])
    currentTimeLeft = measureTime
    currentMeasure = []
    for note in tune.events:
        if currentTimeLeft == 0:
            measures.append(currentMeasure)
            currentTimeLeft = measureTime
            currentMeasure = []
        if note.duration:
            duration = float(note.duration[0]) / float(note.duration[1])
        else:
            duration = 0.25
            note.duration = Tune.Duration.QUARTER
        if (currentTimeLeft - duration >= 0):
            currentMeasure.append(note)
            currentTimeLeft -= duration
        else:
            # split the note and add the first one to the current measure
            splitNote1 = note
            splitNote1.setDuration((1,float(1/currentTimeLeft)))
            currentMeasure.append(splitNote1)

            # change the note's duration!
            possibleDurations = [1,.5,.25,0.125,0.0625]
            for d in possibleDurations:
                if (currentTimeLeft - d) >= 0:
                    note.setDuration(1,float(1/currentTimeLeft))
                    currentMeasure.append(note)
            currentMeasure = padMeasureWithRests(currentTimeLeft,currentMeasure)
            measures.append(currentMeasure)
            currentTimeLeft = measureTime
            currentMeasure = []
            # add the second one to the next measure
            #splitNote2 = Tune.Note()
            #splitNote2.pitch = note.pitch
            # 1.duration + 2.duration = note.duration
            #dur2 = duration - float(splitNote1.duration[0])/float(splitNote1.duration[1])
            #if dur2 > 0:
            #    splitNote2.duration = (1, float(1 / dur2))
            #    currentMeasure.append(splitNote2)
            #    currentTimeLeft -= dur2


    if len(currentMeasure) > 0:
        if currentTimeLeft > 0: # insert a rest to fill the measure otherwise abjad throws an exception
            currentMeasure = padMeasureWithRests(currentTimeLeft,currentMeasure)
            #restOfMeasure = measureTime - currentTimeLeft
            #rest = Tune.Rest()
            #rest.setDuration((1,int(1/restOfMeasure)))
            #currentMeasure.append(rest)
        measures.append(currentMeasure)
    return measures


def padMeasureWithRests(currentTimeLeft,currentMeasure):
    while currentTimeLeft > 0:
        rest = Tune.Rest()
        rest.setDuration(Tune.Duration.SIXTEENTH)
        currentMeasure.append(rest)
        currentTimeLeft -= 0.0625
    return currentMeasure

# FOR PARSING CHORDS
# ps = []
# chord = abjad.Chord([], abjad.Duration(duration[0], duration[1]))
# for pitch in pitches:
#     letter = pitch.letter
#     accidental = ""
#     if pitch.accidental == Tune.Accidental.FLAT:
#         accidental += "b"
#     elif pitch.accidental == Tune.Accidental.SHARP:
#         accidental += "#"
#     octave = str(pitch.octave)
#
#     chord.note_heads.append(abjad.pitchtools.NamedPitch(letter.upper() + accidental + octave))
#
# staff = abjad.Staff([chord])
# abjad.show(staff)


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
        staff = makeStaffFromTune(tune) #abjad.Staff(notes)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
        lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
        return lilypond_file

def makeStaffFromTune(tune):
    # TODO milestone 4b Rachel

    global measuresObj

    time_signature = abjad.TimeSignature(tune.getTimeSignature())
    if time_signature is None:
        time_signature = abjad.TimeSignature(4,4)

    # now coming as a list of lists so notes separated by measure
    notes = tuneToNotes(tune)

    savedMeasures = []
    staff = abjad.Staff()
    for measure in notes:
        #print aEvent.written_duration
        m = abjad.Measure(time_signature, measure)
        m = abjad.scoretools.append_spacer_skip_to_underfull_measure(m)
        d = m._preprolated_duration
        if d == time_signature.duration:
            staff.append(m)
            savedMeasures.append(m)
        #staff.append(abjad.Measure(abjad.Measure(time_signature,measure)))
    measuresObj = savedMeasures

    #c = abjad.Chord("<c'>8")
    #measure = abjad.Measure(abjad.TimeSignature((1,8)),[c])
    #staff.append(measure)
    #print staff

    #time_signature = abjad.TimeSignature(tune.getTimeSignature())
    #if time_signature:
    #    abjad.attach(time_signature, staff)
    key = tune.getKey()
    if key:
        if key.isMajor:
            key_signature = abjad.KeySignature(key.pitch.letter,"major")
        else:
            key_signature = abjad.KeySignature(key.pitch.letter, "minor")
        abjad.attach(key_signature, staff)

    clef = tune.clef
    if clef == Tune.Clef.BASS:
        c = abjad.Clef('bass')
    else:
        c = abjad.Clef('treble')
    abjad.attach(c, staff)

    return staff

# lilypond representation has changed so need to prepare to save a new pdf
def updatePDFWithNewLY(lilypond_file):
    saveLilypondForDisplay(lilypond_file)
    # timestamp for pdf name
    filenamePDF = time.strftime("%d%m%Y") + time.strftime("%H%M%S")
    #delete the old file so only one file in currentTune folder at a time
    oldFilenameFile = open("static/currentTune/oldFilename.txt", 'r')
    oldFilename = ""
    for line in oldFilenameFile:
        oldFilename = line
    #now write the new file name to oldFilename.txt
    oldFilenameFile = open("static/currentTune/oldFilename.txt", 'w')
    oldFilenameFile.write(filenamePDF)
    # save the pdf
    abjad.systemtools.IOManager.save_last_pdf_as("static/currentTune/" + filenamePDF + ".pdf")
    # delete the old file
    subprocess.Popen(["rm", "static/currentTune/" + oldFilename + ".pdf"])
    # return what the pdf is called
    return filenamePDF

def validTitleOrNames(str):
    if str == "":
        return False
    if str.isspace():
        return False
    if "\\n" in str:
        return False
    if len(str) > 128:
        return False
    return True


if __name__ == "__main__":
    tuneObj = None
    app.debug = True
    app.run(port=1995)


def setTune(tune):
    global tuneObj
    tuneObj = tune

def getTune():
    global tuneObj
    return tuneObj

