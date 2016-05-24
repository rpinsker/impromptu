import math
import itertools
import sys
import abc
import json
import pprint
from TuneIter2 import *

#tune = Tune.TuneWrapper('../tests/MIDITestFiles/c-major-scale-treble.mid')
#print tune.TunetoString()
#tune.TunetoJSON()
#pprint.pprint(tune.events)

tune2 = Tune.TuneWrapper('../tests/MIDITestFiles/d-flat-major-scale-on-treble-clef.mid')
print tune2.TunetoString()
tune2.TunetoJSON()
pprint.pprint(tune2.events)

#fp = open("../tests/MIDITestFiles/tune.json")
#JSONtoTune(fp)
#file1 = '../tests/MIDITestFiles/tune-with-chord-rest-note.mid'
#tune = Tune.TuneWrapper(file1)
#print tune.TunetoString()


