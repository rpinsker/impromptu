import math
import itertools
import sys
import abc
import json
import pprint
from TuneSubclasses import *
from Tune import *

#gtg
#tune = Tune.TuneWrapper('../tests/MIDITestFiles/c-major-scale-treble.mid')
#print tune.toString()
#tune.TunetoJSON()
#tune_json = Tune()
#tune_json.JSONtoTune('../src/tune-generic.json')
#tune_json.toString()
#tune_json.TunetoJSON()

#gtg
#tune2 = Tune.TuneWrapper('../tests/MIDITestFiles/d-flat-major-scale-on-treble-clef.mid')
#print tune2.toString()
#tune2.TunetoJSON()
#tune2_json = Tune()
#tune2_json.JSONtoTune('../src/tune-generic.json')
#print tune2_json.toString()

#gtg
#tune3 = Tune.TuneWrapper('../tests/MIDITestFiles/tune-with-chord-rest-note.mid')
#print tune3.toString()
#tune3.TunetoJSON()
#tune3_json = Tune()
#tune3_json.JSONtoTune('../src/tune-generic.json')
#print tune3_json.toString()

#gtg
tune4 = Tune()
tune4.JSONtoTune("../tests/MIDITestFiles/tune.json")
print tune4.toString()
tune4.TunetoJSON()



