import cmd
import coltrane


class Shell(cmd.Cmd):
    """The main interface for the Coltrane music theory library"""

    prompt = "♯ "
    
    def __init__(self):
        super(Shell, self).__init__()
        
    def do_scale(self, s):
        args = s.split(" ")
        args[0] = args[0][0].upper() + args[0][1:]
        if Shell.checkArgs(args, 2):
            if len(args) != 2:
                print("Error")
            print(coltrane.ToneCollection(coltrane.Scale(*args)).prettySequence())

    def help_scale(self):
        print("Prints the notes in a given scale. \n\
            Syntax:   scale <key> <mode>\n\
            Examples: scale Eb major\n\
                      scale A ionian")

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