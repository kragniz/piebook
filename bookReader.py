#/usr/bin/env python
#A small text-based ebook reader
import curses, sys, time, traceback

class Book(object):
    '''Handle reading and manipulating lines from a text file'''
    def __init__(self, textFileName):
        '''Create a book object'''
        self.lineLength = 80
        self.text = open(textFileName, 'r')
        
        self.w = [] #words left over from the last line
        
    def setLineLength(self, length):
        '''Set the length of each line of the output'''
        self.lineLength = length
        
    def _checkLength(self, line):
        return (len(line) <= self.lineLength)
    
    def _split(self, line):
        '''Split a string into substrings. Much simpler than Str.split(), keeps whitespace.'''
        l = []
        i = ''
        for c in line:
            if c == ' ':
                l += [i+' ']
                i = ''
            else:
                i += c
        l += [i]
        return l
                
    def line(self):
        '''Return the next line'''
        line = []
        words = []
        
        if self.w:
            while self._checkLength(''.join(line)) and self.w:
                line += [self.w.pop(0)]
                
        else:
            if self._checkLength(''.join(line)):
                words = self._split(self._nextLine())
                while self._checkLength(''.join(line)) and words:
                    line += [words.pop(0)]
            else:
                self.w = [line.pop(-1)] + self.w
            
        while not self._checkLength(''.join(line)):
            self.w = [line.pop(-1)] + self.w
            
        self.w += words
        
        return ''.join(line).replace('\n', '')
            
    def _nextLine(self):
        '''Return a single line from the book'''
        return self.text.readline()
    
class BookHistory(object):
    '''Make and write the settings/progress for a particular book'''
    def __init__(self):
        self._bookFileName = ''
        self._lineNumber = 0
        
    def read(self, historyFileName):
        f = open(historyFileName).readlines()
        d = []
        for line in f:
            if '#' in line: #handle some comments
                d += [line[:line.index('#')].strip()] #allow the comment to start on a line of code
            else:
                d += [line.strip()]
        while '' in data:
            d.remove('')
            
        d = [l.lower() for l in d]
        
        for l in d:
            if l.startswith('currentLine'):
                self._lineNumber = l[12:]
    
class BookReader(object):
    '''Display the book in a terminal'''
    def __init__(self, screen):
        self.screen = screen
        self.book = Book('example.txt')
        
        curses.curs_set(0)
        self.cols = curses.COLS
        self.rows = curses.LINES
        
        i = 0
        lastLine = ''
        while True:
            thisLine = self.book.line()
            self.drawLine(lastLine, i)
            if i+2 >= curses.LINES:
                i = 0
            else:
                i += 1
            self.drawNewLine(thisLine, i)
            lastLine = thisLine
            time.sleep(0.2)
        
    def drawNewLine(self, line, y, x=0):
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.A_UNDERLINE)
        self.refresh()
        
    def drawLine(self, line, y, x=0):
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.color_pair(0))
        self.refresh()
        
    def refresh(self):
        self.screen.refresh()

if __name__ == '__main__':
    #Main program bits
    if len(sys.argv) > 1:
        if sys.argv[1] == 'book':
            book = Book('example.txt')
            for i in range(30):
                print book.line()
                
        if sys.argv[1] == 'history':
            history = BookHistory()
            history.read()
            
    else:
        def main(stdscr):
            #foreground/background colour pair
            #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            return BookReader(stdscr)
        
        curses.wrapper(main)
    
