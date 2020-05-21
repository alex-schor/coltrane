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

        print(coltrane.Scale.smartParse(*args).prettySequence())

    def help_scale(self):
        print("Prints the notes in a given scale. \n\
            Syntax:   scale <key> <mode>\n\
            Examples: scale Eb major\n\
                      scale A ionian")

    def do_chord(self, s):
        if "#" in s:
            args = s[:s.rfind("#")+1], s[s.rfind("#")+1:]
        elif "b" in s:
            args = s[:s.rfind("b")+1], s[s.rfind("b")+1:]
        else:
            args = s[0], s[1:]

        print(coltrane.Chord(*args).prettySequence())

    def help_chord(self):
        print("Prints the notes in a given chord. \n\
            Syntax:   chord <root><quality>\n\
            Examples: chord Eb7\n\
                      chord Am7b9#5")

    def do_c(self,s):
        self.do_chord(self, s)

    def help_c(self):
        print("Shortcut for chord")

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