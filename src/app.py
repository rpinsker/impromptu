
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
notesObj = None
impromptuMeasuresObj = None

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
    subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.png"))
    subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.ly"))
    # SAVE AS A PNG
    name = time.strftime("%d%m%Y") + time.strftime("%H%M%S")
    result = abjad.topleveltools.persist(expr).as_png('static/currentTune/'+ name + '.png',**kwargs)
    return 'static/currentTune/'+ name + '.png'


@app.route('/', methods=['GET', 'POST'])
def tune():
    global tuneObj
    # make a lilypond file, either from tune object previously created or
    # a filler one when page is first loaded
    lilypond_file = makeLilypondFile(tuneObj)
    tuneObj.TunetoJSON(filename='static/uploads/currentTune.json')
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
            tuneObj.TunetoJSON(filename='static/uploads/currentTune.json')
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')
        # change the contributors. update lilypond file and backend storage of tune object accordingly
        if request.form.has_key('contributorsInput'):
            composer = str(request.form['contributorsInput'])
            if validTitleOrNames(composer):
                lilypond_file.header_block.composer = abjad.markuptools.Markup(composer)
                if tuneObj:
                    tuneObj.contributors = composer
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            tuneObj.TunetoJSON(filename='static/uploads/currentTune.json')
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
                tuneObj.TunetoJSON(filename='static/uploads/currentTune.json')
                return render_template('home.html',filename='static/currentTune/' + filenamePDF + '.pdf',measures=listOfMeasures)


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
                tuneObj.TunetoJSON(filename='static/uploads/currentTune.json')
                return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf')

        if request.form.has_key('note-submit') and request.form.has_key('measure_number') and request.form.has_key('note_number'):
            measureIndex = request.form['measure_number']
            noteIndex = request.form['note_number']
            dur0 = request.form['duration0']
            dur1 = request.form['duration1']
            letter = request.form['pitch']
            letter = str(letter)
            if letter == "Rest":
                letter = "r"
            accidental = request.form['acc']
            accidental = str(accidental)
            if accidental == "&#9839;":
                accidental = 1
            elif accidental == "&#9837;":
                accidental = 2
            else:
                accidental = 0
            octave = str(request.form['octave'])
            type = str(request.form['submit-type'])
            if type == "edit":
                editDurationUpdateTuneObj(int(measureIndex) - 1,int(noteIndex) - 1,int(dur0),int(dur1))
                editPitchUpdateTuneObj(int(measureIndex) - 1, int(noteIndex) - 1, letter.lower(), accidental, int(octave))
            elif type == "add":
                addNoteUpdateTuneObj(int(measureIndex) - 1, int(noteIndex) - 1, int(dur0), int(dur1), letter.lower(), accidental, int(octave))
            else:
                deleteNoteUpdateTuneObj(int(measureIndex) - 1,int(noteIndex) - 1)
            tune = tuneObj
            # convert our tune object to notes for abjad and then to a staff
            staff = makeStaffFromTune(tune)  # abjad.Staff(notes)
            # make lilypond file, setting title and contributors, and then make the PDF
            lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
            lilypond_file.header_block.title = abjad.markuptools.Markup(tuneObj.title)
            lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
            filenamePDF = updatePDFWithNewLY(lilypond_file)
            listOfMeasures = tunetoMeasures(tuneObj)
            return render_template('home.html', filename='static/currentTune/' + filenamePDF + '.pdf', measures=listOfMeasures)


    # page was loaded normally (not from a request to update name, contributor, or file upload)
    listOfMeasures = tunetoMeasures(tuneObj)
    # so display the tune object created at the beginning of the this method
    filenamePDFTemp = updatePDFWithNewLY(lilypond_file)
    return render_template('home.html',filename='static/currentTune/' + filenamePDFTemp + '.pdf', measures=listOfMeasures)

#
#
# @app.route('/savejson', methods=["GET"])
# def savejson():
#     global tuneObj
#     jsonFilename = tuneObj.TunetoJSON()
#     print "here:", filename
#     return send_from_directory(directory="", filename=filename)
#


@app.route('/measure', methods=["GET","POST"])
def measure():
    if request.method == "POST":
        data = request.form.keys()[0]
        return measureIndexToPNGFilepath(data)

# prepare to save a png for the given measure
def measureIndexToPNGFilepath(i):
    i = int(i) - 1
    if i < len(measuresObj) and i >= 0:
        m = measuresObj[i]
        return save_measure_as_png(m,i+1)
    else:
        return "bad index!"


# editing duration of a note
def editDurationUpdateTuneObj(measureIndex,noteIndex,newDuration0,newDuration1):
    global tuneObj
    global impromptuMeasuresObj

    makeStaffFromTune(tuneObj)
    # update the note in our measures
    m = impromptuMeasuresObj[measureIndex]
    e = m[noteIndex]
    e.setDuration((newDuration0,newDuration1))
    m[noteIndex] = e
    impromptuMeasuresObj[measureIndex] = m

    # make an array of all notes and recompute everything
    events = []
    for measure in impromptuMeasuresObj:
        for event in measure:
            events.append(event)

    # update the global tune object for display
    tuneObj.setEventsList(events)


def editPitchUpdateTuneObj(measureIndex, noteIndex, letter, accidental, octave):
    global tuneObj
    global impromptuMeasuresObj

    makeStaffFromTune(tuneObj)
    # update the note in our measures
    m = impromptuMeasuresObj[measureIndex]
    e = m[noteIndex]
    newPitch = Tune.Pitch()
    newPitch.letter = letter
    newPitch.accidental = accidental
    newPitch.octave = octave
    e.setPitch(newPitch)
    m[noteIndex] = e
    impromptuMeasuresObj[measureIndex] = m

    # make an array of all notes and recompute everything
    events = []
    for measure in impromptuMeasuresObj:
        for event in measure:
            events.append(event)

    # update the global tune object for display
    tuneObj.setEventsList(events)

def addNoteUpdateTuneObj(measureIndex, noteIndex, newDuration0, newDuration1, letter, accidental, octave):
    global tuneObj
    global impromptuMeasuresObj

    makeStaffFromTune(tuneObj)


    newEvent = Tune.Note()

    newEvent.duration = (int(newDuration0), int(newDuration1))
    newPitch = Tune.Pitch()
    newPitch.letter = letter
    newPitch.accidental = accidental
    newPitch.octave = octave
    newEvent.setPitch(newPitch)
    print newPitch.toString()
    print newEvent.getPitch()[0].toString()
    events = []
    newIndex = 0
    counter = 0
    for measure in range(len(impromptuMeasuresObj)):
        for event in range(len(impromptuMeasuresObj[measure])):
            if measure == measureIndex and event == noteIndex:
                newIndex = counter
            events.append(impromptuMeasuresObj[measure][event])
            counter += 1
    updated_events = events[:newIndex] + [newEvent] + events[newIndex:]
    if updated_events[newIndex + 1]:
        print updated_events[newIndex + 1].onset
        updated_events[newIndex].onset = updated_events[newIndex + 1].onset
    for n in updated_events[newIndex+1:]:
        if n.onset:
            n.onset += (newEvent.duration[0] / newEvent.duration[1])
        else:
            n.onset = 0.0
    # update the global tune object for display
    tuneObj.setEventsList(updated_events)
    # update the note in our measures
    impromptuMeasuresObj = tunetoMeasures(tuneObj)

def deleteNoteUpdateTuneObj(measureIndex, noteIndex):
    global tuneObj
    global impromptuMeasuresObj

    counter = 0
    newIndex = 0
    events = []
    for measure in range(len(impromptuMeasuresObj)):
        for event in range(len(impromptuMeasuresObj[measure])):
            if measure == measureIndex and event == noteIndex:
                newIndex = counter
            events.append(impromptuMeasuresObj[measure][event])
            counter += 1

    for n in events[newIndex + 1:]:
        if n.onset:
            n.onset -= (events[newIndex].duration[0] / events[newIndex].duration[1])
        else:
            n.onset = 0.0
    events.remove(events[newIndex])
    tuneObj.setEventsList(events)
    # update the note in our measures
    impromptuMeasuresObj = tunetoMeasures(tuneObj)

# convert a Tune object to an array of notes usable by abjad
def tuneToNotes(tune):

    global impromptuMeasuresObj

    if tune == None:
        return []

    listOfMeasures = tunetoMeasures(tune)

    impromptuMeasuresObj = listOfMeasures

    aNotes = [] # holds lists of notes corresponding to measures

    for measure in listOfMeasures:
        currentMeasure = []
        for event in measure:
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


# make a list of measures to give to abjad
def tunetoMeasures(tune):
    if tune == None:
        return []
    measures = []
    measureTime = float(tune.getTimeSignature()[0]) / float(tune.getTimeSignature()[1])
    currentTimeLeft = measureTime
    currentMeasure = []
    for note in tune.events:
        # measure is full so add it to the list
        if currentTimeLeft == 0:
            measures.append(currentMeasure)
            currentTimeLeft = measureTime
            currentMeasure = []
        # give a duration if it is empty or use the note's actual duration
        if note.duration:
            duration = float(note.duration[0]) / float(note.duration[1])
        else:
            duration = 0.25
            note.duration = Tune.Duration.QUARTER
        # add the note to the measure
        if (currentTimeLeft - duration >= 0):
            currentMeasure.append(note)
            currentTimeLeft -= duration
        else:
            # split the note and add the first one to the current measure
            splitNote1 = note
            splitNote1.setDuration((1,float(1/currentTimeLeft)))
            currentMeasure.append(splitNote1)

            # change the note's duration so it fits in the measure
            possibleDurations = [1,.5,.25,0.125,0.0625]
            for d in possibleDurations:
                if (currentTimeLeft - d) >= 0:
                    note.setDuration((1,float(1/currentTimeLeft)))
                    currentMeasure.append(note)
            currentMeasure = padMeasureWithRests(currentTimeLeft,currentMeasure)
            measures.append(currentMeasure)
            currentTimeLeft = measureTime
            currentMeasure = []


    if len(currentMeasure) > 0:
        if currentTimeLeft > 0: # insert a rest to fill the measure otherwise abjad throws an exception
            currentMeasure = padMeasureWithRests(currentTimeLeft,currentMeasure)
        measures.append(currentMeasure)
    return measures


# add rests until measure fits with time signature
def padMeasureWithRests(currentTimeLeft,currentMeasure):
    while currentTimeLeft > 0:
        rest = Tune.Rest()
        rest.setDuration(Tune.Duration.SIXTEENTH)
        currentMeasure.append(rest)
        currentTimeLeft -= 0.0625
    return currentMeasure


# makes a lilypond file either from globally stored tune object or makes a filler
# staff and pdf to display when page is first loaded
def makeLilypondFile(tune):
    global tuneObj
    # if no tune, make a default one and return the lilypond file
    if tune == None:
        eventsList = []
        curr_onset = 0.0
        for (l,a) in [('g',Tune.Accidental.NATURAL),('a',Tune.Accidental.NATURAL),('c',Tune.Accidental.SHARP),('d',Tune.Accidental.FLAT),('e',Tune.Accidental.NATURAL),('f',Tune.Accidental.FLAT),('g',Tune.Accidental.NATURAL),('a',Tune.Accidental.NATURAL)]:
            dur = Tune.Duration.QUARTER
            p = Tune.Pitch()
            p.letter = l
            p.octave = 4
            p.accidental = a
            note = Tune.Note(duration=dur, pitch=p, onset=curr_onset)
            curr_onset += 0.25
            eventsList.append(note)
        newTune = Tune.Tune()
        newTune.setEventsList(eventsList)
        newTune.setTitle("default")
        tuneObj = newTune
        staff = makeStaffFromTune(newTune)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup("SAMPLE TUNE DISPLAY")
        return lilypond_file
    # use the tune supplied to make a lilypond file
    else:
        notes = tuneToNotes(tune)
        staff = makeStaffFromTune(tune)
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.title = abjad.markuptools.Markup(tune.title)
        lilypond_file.header_block.composer = abjad.markuptools.Markup(tune.contributors)
        return lilypond_file

def makeStaffFromTune(tune):
    global measuresObj

    measuresObj = []

    time_signature = abjad.TimeSignature(tune.getTimeSignature())
    if time_signature is None:
        time_signature = abjad.TimeSignature(4,4)

    # now coming as a list of lists so notes separated by measure
    notes = tuneToNotes(tune)

    # make the measures through abjad and make sure the timing is correct
    savedMeasures = []
    staff = abjad.Staff()
    for measure in notes:
        m = abjad.Measure(time_signature, measure)
        m = abjad.scoretools.append_spacer_skip_to_underfull_measure(m)
        d = m._preprolated_duration
        if d == time_signature.duration:
            staff.append(m)
            savedMeasures.append(m)
    measuresObj = savedMeasures

    # set key and clef
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

