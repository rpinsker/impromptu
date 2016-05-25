import math
import itertools
import sys
import abc
import json
import pprint
from TuneSubclasses import *
from Tune import *

#tune = Tune.TuneWrapper('../tests/MIDITestFiles/c-major-scale-treble.mid')
#print tune.toString()
#tune.TunetoJSON()
#pprint.pprint(tune.events)

#tune2 = Tune.TuneWrapper('../tests/MIDITestFiles/d-flat-major-scale-on-treble-clef.mid')
#print tune2.toString()
#tune2.TunetoJSON()
#pprint.pprint(tune2.events)

#tune3 = Tune.TuneWrapper('../tests/MIDITestFiles/tune-with-chord-rest-note.mid')
#print tune3.toString()
#tune3.TunetoJSON()
#pprint.pprint(tune3.events)

#tune4 = Tune()
#tune4.JSONtoTune("../tests/MIDITestFiles/tune2.json")
#print tune4.toString()
#tune4.TunetoJSON()



#fp = open("../tests/MIDITestFiles/tune.json")
#JSONtoTune(fp)
#file1 = '../tests/MIDITestFiles/tune-with-chord-rest-note.mid'
#tune = Tune.TuneWrapper(file1)
#print tune.toString()


