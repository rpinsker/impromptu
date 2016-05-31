impromptu
interactive music notation


Team members: Ivy Malao, Zoë Naidoo, Annie Chen (Mengyuan Chen), Rachel Pinsker, Zakir Gowani, Sofia Wyetzner

 README
 ** Please see uploaded README PDF as that contains our intended formatting **
1) Installation
Code can be checked out from our Github repository at https://github.com/rpinsker/impromptu
Library dependencies to be downloaded and installed:
LilyPond (Macs: http://lilypond.org/macos-x.html, Windows: http://lilypond.org/windows.html) Follow the directions: “Running on the command-line”
Abjad 2.17 (http://abjad.mbrsi.org/) run “pip install abjad”
Flask (http://flask.pocoo.org/) run “pip install Flask”
Python-midi (https://github.com/vishnubob/python-midi) Download and extract the ZIP located at the GitHub link. Change into the directory and run “python setup.py install”
Aubio 0.4.2 (http://aubio.org/download) and follow the instructions in the aubio readme file:
    ./waf configure
    ./waf build
    sudo ./waf install
If waf is not found in the directory, you can download and install it with:
    make getwaf

*Note: Installation and compilation of the Impromptu web app has only been tested on Macs and not on Windows or Linux machines.

In addition, it is recommended to use Google Chrome, as some functionality may be lost when using other browsers.

2) Functionality Overview
Upload MIDI format 1, WAVE, or Impromptu JSON files and Impromptu will display editable sheet music.
Record audio using the Impromptu interface and a WAVE file will be generated and saved to your browser’s default download folder (which can then be uploaded into Impromptu)
Edit the title of the piece and names of contributors of your sheet music.
Edit, add, and delete events (i.e., notes, rests) to update your sheet music.  An event’s duration, octave and accidental are fields that can be edited.
Save your sheet music as a PDF or as an Impromptu JSON file (also saved to your browser’s default download folder) that can be re-uploaded for continued editing.

3) Software Use Tutorial
Begin by running the app by running “python app.py” in the src folder and visiting http://127.0.0.1:1995/ where the web application should be running on your localhost. A sample tune will be displayed.
To get started, upload your own file.  If you have a MIDI Format 1 or WAVE file handy, go ahead and upload using the “UPLOAD A FILE” button in the lower right hand corner.
 If you do not have a file ready, or would prefer to record your own, click the “RECORD AUDIO” button in the upper right hand corner to begin recording.  The button will display red while the user is recording.  To stop recording press the “RECORD AUDIO” button again and the button will return to white.  The “SAVE AUDIO” button below will highlight to demonstrate that your audio file can now be saved.  Click the button to save the file to your “Downloads” folder.  This file can now be uploaded as in step 2 above.
You can change the title and add contributors by filling in the corresponding text box fields on the upper right hand side of the web page.  Set the fields by pressing the arrow to the right of the text boxes or by pressing enter when the cursor is within the box.  These fields should display at the top of the generated sheet music after a brief pause.
Your music can be edited using the interface on the middle right of the web page.  Please select the number of the measure that you would like to edit and press the “EDIT” button.  Inside the editing interface you will see your chosen measure displayed.
To delete a note select the number of the note that you would like to delete and select “DELETE.” A description of the note’s pitch, octave and duration will be displayed to confirm.  In order to view the effects of this delete press “APPLY” to see it rendered in the editing interface.  To save these changes in the entire score press “SUBMIT” and you will return to the web page with your changes rendered.  Otherwise press “CANCEL” and return to the web page with no changes made.
To edit a note select the number of the note that you would like to edit and select “EDIT.” A description of the note’s pitch, accidental, octave  and duration will be displayed to edit using the drop down arrows.  In order to view the effects of this edit press “APPLY” to see it rendered in the editing interface.  To save these changes in the entire score press “SUBMIT” and you will return to the web page with your changes rendered.  Otherwise press “CANCEL” and return to the web page with no changes made.
To add a note select the index the note before which the new note should be placed and select “ADD.” The new note’s pitch, accidental, octave  and duration will be displayed to be edited using the drop down arrows.  In order to view the effects of this add press “APPLY” to see it rendered in the editing interface.  To save these changes in the entire score press “SUBMIT” and you will return to the web page with your changes rendered.  Otherwise press “CANCEL” and return to the web page with no changes made.
To save your sheet music as a JSON file that can be edited later press the “SAVE JSON” button in the middle left hand side of the web page.  A JSON file with your sheet music will be saved to your browser’s downloads folder.  In order to edit this sheet music at a later time, just press the “LOAD JSON” button to load the JSON file back into the Impromptu app.  The sheet music should be displayed just as before and can be edited as usual.
(In Chrome) In order to download your final cut of sheet music as a PDF, press the downwards facing arrow (downloads icon) directly above the sheet music on the black bar
(In Chrome) In order to print your final cut of sheet music, press the small printer icon directly above the sheet music on the black bar

4) Unsupported inputs
The only durations that are supported are: Sixteenth, Eighth, Quarter, Half, Whole
You can only upload MIDI format 1 files and not format 0 or 2.
You cannot upload an MP3 file, but there are many online converters to convert MP3 to WAVE.
While a WAVE file with multiple layers of sound including chords can be uploaded, they will not be rendered accurately and only the most prominent pitch will be rendered.
Chords cannot be edited (although notes within them can be).
Note durations are adjusted in order to fit into measures as determined by the time signature, this sometimes involves adding rests that were not in the original music, and abridging notes that were previously longer (this sometimes affects the editing capabilities as well)
Refreshing the page after uploading sheet music can cause server errors, so save work in the JSON format and rerun the application instead
