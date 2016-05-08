#  Tune(.mid file, timeSignature, clef, “title”, [“Contributors”], Key): Tune
# +tunetoJSON(): file<file.json>
# + readFrequency(MIDI[i]): float
# + readOnset(MIDI[i]): float

class Clef:
	TREBLE, BASS = range(2)

class Accidental:
	SHARP, FLAT, NATURAL = range(3)



# refer to vartec's answer at http://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
class Tune:
	# classVariable = 'something' # class variable shared by all instances
	def __init__(self, **kwargs):
		self.midi = kwargs.get('midi', default=None)
		self.notes = []
		self.timeSignature = kwargs.get('timeSignature', default=(4, 4))
		self.keySignature = kwargs.get('keySignature', default=Key(True, Pitch('c')))
		self.clef = kwargs.get('clef', default=Clefs.TREBLE)
		self.title = kwargs.get('title', default='Insert Title')
		self.contributors = kwargs.get('contributors', default=['Add Contributors'])

class Tune2:
	# classVariable = 'something' # class variable shared by all instances
	def __init__(self, midi, timeSignature, keySignature, clef, title, contributors):			# instance variable unique to each instance
		self.midi = midi
		self.notes = []
		self.timeSignature = timeSignature
		self.keySignature = keySignature
		self.clef = clef
		self.title = title
		self.contributors = contributors