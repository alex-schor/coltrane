import cmd
import coltrane


class Shell(cmd.Cmd):
    """The main interface for the Coltrane music theory library"""

    prompt = "♯ "
    
    def __init__(self):
        super(Shell, self).__init__()
        
    def do_scale(self, s):
        args = s.split(" ", 1)
        args[0] = args[0][0].upper() + args[0][1:]
        key, name = args
        options = coltrane.Scale.fuzzyParse(name)
        if len(options) == 0:
            print("Sorry, scale name", name, "not found. No similar scale names found.")
        elif len(options) == 1 and options[0][1] == 100:
            print(coltrane.Scale.smartParse(*args).prettySequence())
        else:
            print("Sorry, scale name", name, "not found. Did you mean:")
            for o in options:
                print(o[0])


    def help_scale(self):
        print("Prints the notes in a given scale. \n\
            Syntax:   scale <key> <mode>\n\
            Examples: scale Eb major\n\
                      scale A ionian")

    def do_chord(self, s, vertical=True):
        root = s[0]
        quality = s[1:]
        while quality[0] in ("b", "#"):
            root += quality[0]
            quality = quality[1:]

        root = root[0].upper() + root[1:]
        print(coltrane.Chord(root, quality).prettySequence(vertical=vertical))

    def help_chord(self):
        print("Prints the notes in a given chord.\n\
            Syntax:   chord <root><quality>\n\
            Examples: chord Eb7\n\
                      chord Am7b9#5")

    def do_c(self,s):
        self.do_chord(s)

    def help_c(self):
        print("Shortcut for chord")

    def do_progression(self,s):
        for c in s.split(" "):
            self.do_chord(c, vertical = False)

    def do_cp(self,s):
        self.do_progression(s)



    def do_s(self,s):
        self.do_scale(s)

    def help_s(self):
        print("Shortcut for scale")

    def do_exit(self, s):
        return True

    def help_exit(self):
        print("Exits the CLI")

    def checkArgs(args, exact_count=None, min_count=None, max_count=None):
        if exact_count is not None and len(args) != exact_count:
            print("Expected exactly", exact_count, "args, instead got", len(args))
            return False
        if min_count is not None and len(args) < min_count:
            print("Expected at least", min_count, "args, instead got", len(args))
            return False
        if max_count is not None and len(args) > max_count:
            print("Expected at most", max_count, "args, instead got", len(args))
            return False
        return True



try:
    Shell().cmdloop()
except KeyboardInterrupt as e:
    print("exit")