
def parse_

class ParserError(Exception):
    def __init__(self, message, line, filename=None, line_text=None):
        if line:
            message += ' at line %d' % line
            if line_text:
                message += ": '%s'" % line_text.strip()
        super(ParserError, self).__init__(message)
        self.line = line
        self.line_text = line_text
        self.filename = filename

    def __str__(self):
        if self.filename:
            return 'Failed to parse "%s": %s' % (self.filename, self.args[0])
        return 'Failed to parse <string>: %s' % self.args[0]


class Parser(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'init'
        self.line = 0
        self.last_step = None

        self.filename = None
        self.test = None
        self.tags = []
        self.lines = []

    def parse(self, data, filename):
    	self.reset()
        self.filename = filename

        for line in data.split('\n'):
            self.line += 1
            if not line.strip() and not self.state == 'multiline':
                # -- SKIP EMPTY LINES, except in multiline string args.
                continue
            self.action(line)

        if self.table:
            self.action_table('')

        feature = self.feature
        if feature:
            feature.parser = self
        self.reset()
        return feature