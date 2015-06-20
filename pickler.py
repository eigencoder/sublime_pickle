import cPickle as pickle
import pprint
#import sublime
import sublime_plugin

#Cheat because I don't understand how self/view should be passed
INDENT_SIZE = None
def get_indent_size(view):
    return int(view.settings().get('tab_size', 2))

#Get file encoding?

class Transformer(sublime_plugin.TextCommand):
    def run(self, edit):
        if not INDENT_SIZE:
            global INDENT_SIZE
            INDENT_SIZE = get_indent_size(self.view)
        self.transform(self.transformer[0], self.view, edit)

    def transform(self, f, view, edit):
        for s in view.sel():
            if s.empty():
                s = view.word(s)

            txt = f(view.substr(s))
            # Only replace text if there's a result?
            view.replace(edit, s, txt)

def unpickle(s):
    s = s.encode("UTF-8") # s is unicode, switch to string
    s = s.replace('\\n', '\n') # replace \n character pair with a real newline character
    data = pickle.loads(s)
    if not pprint.isreadable(data):
        print "Data cannot be loaded as it is not yield a good representation of pickle. (isreadable false)"
        return data
    pretty_data = pprint.pformat(data, indent=INDENT_SIZE)
    return pretty_data

def do_pickle(s):
    #WARNING: EVAL !!!
    #Code being evaluated could break SublimeText or delete files on your computer!
    data = eval(s)
    return pickle.dumps(data)


class UnpickleCommand(Transformer):
    transformer = lambda s: unpickle(s),

class PickleCommand(Transformer):
    transformer = lambda s: do_pickle(s),

