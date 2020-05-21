"""
coltrane.py
A collection of utilities for music theory operations in Python

Alex Schor
5/18/2020
"""


#=================================================================================================#

class Tone:
    """
    A class representing a Tone object. Contains a tone name (C#, Db, etc.) and a "value" (the
    number of half steps above C0). The default equality operation (==) does not consider enharmonic
    tones equivalent (E# != Db), but the .equals() method does (E#.equals(Db) is true)."""

    letters = ["C", "D", "E", "F", "G", "A", "B"]

    tones = {
        "C":    0,
        "C#":   1,
        "Db":   1,
        "D":    2,
        "D#":   3,
        "Eb":   3,
        "E":    4,
        "Fb":   4,
        "E#":   5,
        "F":    5,
        "F#":   6,
        "Gb":   6,
        "G":    7,
        "G#":   8,
        "Ab":   8,
        "A":    9,
        "A#":   10,
        "Bb":   10,
        "B":    11,
        "Cb":   11,
    }

    values = {
        0 : ("C" ,          ),
        1 : ("C#",  "Db"    ),
        2 : ("D" ,          ),
        3 : ("D#",  "Eb"    ),
        4 : ("E" ,  "Fb"    ),
        5 : ("E#",  "F"     ),
        6 : ("F#",  "Gb"    ),
        7 : ("G" ,          ),
        8 : ("G#",  "Ab"    ),
        9 : ("A" ,          ),
        10: ("A#",  "Bb"    ),
        11: ("B" ,  "Cb"    )
    }

    name = ""
    value = None

    def __init__(self, n, v = None, prefer_sharp = False):
        """Initializes a Tone object
        
        Args:
            n (str, int, Tone): The tone's name or value. Providing one will assume the other. If
            you specify the value for E#/Db4, the prefer_sharp flag will be used to determine which
            name to use. If no octave is specified in the name the octave will be assumed to be
            zero.
            
            v (None, optional): If you specify a name as the first argument, you can specify a value
            in the second. This allows you to specify which of the enharmonic equivalent names will
            be used.

            prefer_sharp (bool, optional): When only a value is provided, if the prefer_sharp is
            true the program will try to find a sharp name for the tone. This only applies if the
            two options are one sharp and one flat (e.g. D# and Eb). If a natural tone name is
            available it will be used. You can use two arguments in the constructor or use
            getEnharmonicTones or getEnharmonic to change the name of the tone.

        """
        if isinstance(n, Tone):
            self.name = n.name
            self.value = n.value
    
        elif v is not None and isinstance(v, int):
            self.name = Tone(n).name
            self.value = v
    
        elif isinstance(n, str):
            self.name, self.value = Tone.nameToValue(n, clean_name=True)

    
        elif isinstance(n, int):
            self.value = n
            self.name = Tone.valueToName(n, prefer_sharp)

    def nameToValue(s, clean_name=False):
        """Gets the tone value (half steps above C0) given a tone name as a string
        
        Args:
            s (str): The name of the tone (e.g "E#4")
        
        Returns:
            int: the tone value
        """

        # TODO: add support for double sharp, etc.
        # TODO: add support for two-digit octave numbers
        
        octave = 0
        if (s[-1].isdigit()):
            octave = int(s[-1])
            s = s[:-1]

        value = Tone.tones[s] + octave * 12
        if clean_name:
            return s, value
        else:
            return value

    def valueToName(v, prefer_sharp = False):
        """Gets the string name of the tone ("E#") given its integer value
        
        Args:
            v (int): the tone's integer value (half steps above C0)
            prefer_sharp (bool, optional): if true the program will try to find a sharp name for the
            tone. This only applies if the two options are one sharp and one flat (e.g. D# and Eb).
            If a natural tone name is available it will be used.

        Returns:
            str: The name that corresponds to the given value
        """
        v = (v % len(Tone.values))
        options = Tone.values[v]
        if len(options)>1:
            natural = None
            sharp = None
            flat = None
            for o in options:
                if "#" in o:
                    sharp = o
                elif "b" in o:
                    flat = o
                else:
                    natural = o
            if natural is not None:
                return natural
            elif prefer_sharp and sharp is not None:
                return sharp
            else:
                return flat
        else:
            return options[0]


    def getLetter(self):
        """Gets the string base letter of the Tone given the Tone object (e.g. Tone("C#") => "C")
        
        Returns:
            str: The letter of the Tone
        """
        return self.name[0]

    def getName(self):
        """Returns the string name of the tone, without the octave number (e.g. Tone("C#4") => "C#")
        
        Returns:
            str: The name of the tone
        """
        return self.name

    def getFullName(self):
        """Returns the string name of the tone, including the tone's octave number (e.g. Tone("C#4")
        => "C#4")
        
        Returns:
            str: The name of the tone
        """
        return self.name + str(self.getOctave())

    def getInterval(self, other, octmod = False):
        """Returns the integer interval, in half-steps, between the tone and another tone 
        
        Args:
            other (Tone): The other tone
            octmod (bool, optional): If true, it will ignore octave differences (e.g.
            A#0.getInterval(C4) => 2)
        
        Returns:
            int: The number of half-steps between the two tones
        """
        if octmod:
            return (other.value % 12) - (self.value % 12)
        else:
            return (other.value - self.value)

    def getSharpened(self):
        """Sharpens the tone (raises by a half-step) and returns a new Tone object
        
        Returns:
            Tone: A new tone, equal to the old tone raised by one half-step
        """
        new = Tone(self.value + 1, prefer_sharp = True)
        return new

    def getFlattened(self):
        """Flattens the tone (lowers by a half-step) and returns a new Tone object
        
        Returns:
            Tone: A new tone, equal to the old tone lowered by one half-step
        """
        new = Tone(self.value - 1, prefer_sharp = False)
        return new

    def getOctave(self):
        """Returns the octave number of the tone (e.g. C4 => 4)
        
        Returns:
            int: the octave number of the tone object
        """
        return self.value // 12

    def setOctave(self, octave):
        """Transposes the tone into the given octave number
        
        Args:
            octave (int): The octave number to transpose to
        """
        curOctave = self.getOctave()
        self.value += 12*(octave - curOctave)

    def getAdjacentLetters(self):
        """Gets the adjacent letters (basically adjacent two tones in the Cmaj scale) (e.g F# => 
        (E,G))
        
        Returns:
            str tuple: the two string letters
        """
        i = Tone.letters.index(self.getLetter())
        n = (i + 1) % len(Tone.letters)
        p = (i - 1) % len(Tone.letters)
        adjacents = (Tone.letters[p], Tone.letters[n])
        return adjacents

    def getNextLetter(self):
        """Gets the next letter in the Cmaj scale (e.g. Cb => D)
        
        Returns:
            str: the next letter
        """
        return self.getAdjacentLetters()[1]

    def getPrevLetter(self):
        """Gets the previous letter in the Cmaj scale (e.g. Cb => B)
        
        Returns:
            str: the previous letter
        """        
        return self.getAdjacentLetters()[0]

    def getEnharmonicTones(self):
        """Returns a list of tones enharmonic to the given tone
        
        Returns:
            [Tone]: the tones enharmonic to the given tone
        """
        new = self.copy()
        toneNames = Tone.values[self.value % 12]
        tones = list(Tone(n) for n in toneNames)
        for n in tones:
            n.setOctave(self.getOctave())
        return tones
        # return options

    def getEnharmonic(self):
        """Gets the one tone enharmonic to the given tone. This only considers single flat and sharp
        tones (will never return C##). If no single sharp or flat tones are found, this returns a
        copy of the given tone unaltered.
        Returns:
            Tone: A new Tone object
        """
        for n in self.getEnharmonicTones():
            if not n.equals(self):
                return n
        return self.copy()

    def getNatural(self):
        """Makes the tone natural, removing any accidentals from it (e.g. C# => C)
        
        Returns:
            Tone: The natural tone
        """
        new = self.copy()
        for i in range(new.name.count("#")):
            new.name = new.name[:-1]
            new.value -= 1
        for i in range(new.name.count("b")):
            new.name = new.name[:-1]
            new.value +=1
        return new

    def copy(self):
        """Makes a deep copy of the tone
        
        Returns:
            Tone: A new Tone object
        """
        return Tone(self)

    def equals(self, other, octmod = False):
        """Compates the tone to another tone. Considers enharmonic equivalents to be equal. (e.g.
        C#.equals(Db) is true)
        
        Args:
            other (TYPE): The other Tone object
            octmod (bool, optional): if true, ignores octave differences (e.g. C#4.equals(C#0) is
            true)

        Returns:
            bool: Whether the two Tones are equal
        """
        if octmod:
            return (self.value % 12) == (other.value % 12)
        else:
            return self == other


    def __str__(self):
        return self.getFullName()

    def __eq__(self, other):
        return (self.name == other.name) & (self.value == other.value)


#=================================================================================================#


class Mode:

    ionian = [2,2,1,2,2,2,1]

    modes = {
        "ionian"        : 1,
        "major"         : 1,
        "dorian"        : 2,
        "phrygian"      : 3,
        "lydian"        : 4,
        "mixolydian"    : 5,
        "aeolian"       : 6,
        "minor"         : 6,
        "locrian"       : 7
    }

    values = {
        1 : "ionian",
        2 : "dorian",
        3 : "phrygian",
        4 : "lydian",
        5 : "mixolydian",
        6 : "aeolian",
        7 : "locrian"
    }

    def modeToValue(m):
        return Mode.modes[m]

    def valueToMode(v, prefer_sharp = False):
        return Mode.values[v]

    def valueToSteps(v):
        return Mode.ionian[v-1 : len(Mode.ionian)] + Mode.ionian[0:v-1]


    name = ""
    value = 0
    steps = []

    def __init__(self, m):
        if isinstance(m, str):
            self.name = m
            self.value = Mode.modeToValue(m)
        elif isinstance(m, int):
            self.value = m
            self.name = Mode.valueToMode(m)
        self.steps = Mode.valueToSteps(self.value)


#=================================================================================================#


class ToneCollection(list):
    tones = []
    def __init__(self, tones):
        self.tones = list(Tone(n) for n in tones)

    def __str__(self):
        return str([str(tone) for tone in self.tones])

    def __getitem__(self, i):
        return self.tones[i]

    def __eq__(self, other):
        return self.tones == other.tones

    def __iter__(self):
        for tone in self.tones:
            yield tone

    def index(self, tone, octmod = False):
        for i, n in enumerate(self.tones):
            if (n.equals(tone, octmod)):
                return i
        raise ValueError("Tone " + str(tone) + " not found in ToneCollection")

    def prettySequence(self, include_octaves = False):
        return " ".join([tone.name for tone in self.tones])






#=================================================================================================#


class Scale(ToneCollection): 
    name = ""
    key = None
    mode = None

    def __init__(self, key, mode):
            if not isinstance(key, (Tone, str, int)):
                raise ValueError("Invalid Type: expected key to be Tone, string or int but instead was " + type(key))
            if not isinstance(key, Tone):
                key = Tone(key)

            if not isinstance(mode, (Mode, str, int)):
                raise ValueError("Invalid Type: expected mode to be Mode, string or int but instead was " + type(mode))
            if not isinstance(mode, Mode):
                mode = Mode(mode)
            
            steps = mode.steps
            intervals = [sum(steps[0:i+1]) for i in range(len(steps))]
            values = [key.value] + [key.value + i for i in intervals]
            raw_tones = [Tone(v) for v in values]
            self.tones = Scale.cleanScale(raw_tones, root = key)

    def cleanScale(tones, root=None):
        if root is not None:
            root = Tone(root)
            root.setOctave(tones[0].getOctave())
            if tones[0] != root:
                tones[0] = tones[0].getEnharmonic()

        for i in range(0, len(tones)-1):
            if tones[i+1].getLetter() != tones[i].getNextLetter():
                tones[i+1] = tones[i+1].getEnharmonic()

        return tones




if __name__ == '__main__':
    print(Scale("F#", "major"))
    # print(Tone.valueToName(10))
    # f = Tone("F")
    # es = Tone("E#")
    # print(f.getInterval(es))



#=================================================================================================#




        

