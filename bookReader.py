#/usr/bin/env python
#A small text-based ebook reader
import curses, sys, time, json
from os.path import splitext
from threading import Thread

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
    
    def setPosition(self, lineNumber):
        '''Make lineNumber the current line'''
                
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
        self._historyData = {
            'bookFileName' : '',
            'lineNumber' : 0,
            'speed' : 2.5}
            
    def setBookFile(self, bookFileName):
        self._historyData['bookFileName'] = bookFileName
        
    def setLineNumber(self, n):
        self._historyData['lineNumber'] = n
        
    def setSpeed(self, s):
        self._historyData['speed'] = s
        
    def lineNumber(self):
        return self._historyData['lineNumber']
    
    def incrementLineNumber(self):
        self._historyData['lineNumber'] += 1
        
    def read(self, historyFileName=None):
        '''Read the settings made from a previous run of this program'''
        if not historyFileName:
            historyFileName = splitext(self._historyData['bookFileName'])[0] + '.hst'
            
        data = ''.join(open(historyFileName).readlines())
        self._historyData = json.loads(data)
        
    def write(self, historyFileName=None):
        '''Write the settings for next time the program is run'''
        if not historyFileName:
            historyFileName = splitext(self._historyData['bookFileName'])[0] + '.hst'
            
        f = open(historyFileName, 'w')
        f.writelines(json.dumps(self._historyData, sort_keys=True, indent=4))
        f.close()
    
class BookReader(object):
    '''Display the book in a terminal'''
    def __init__(self, screen):
        self.screen = screen
        self.book = Book('example.txt')
        self.inputThread = InputThread(self.screen)
        self.inputThread.start()
        
        curses.curs_set(0)
        self.cols = curses.COLS
        self.rows = curses.LINES
        self.screen.timeout(0)
        
        i = 0
        lastLine = ''
        while True:
            #keystrokes/commands
            c =  self.screen.getch()
            if c == 'q':
                break
            
            thisLine = self.book.line()
            self.drawLine(lastLine, i)
            if i+2 >= curses.LINES:
                i = 0
            else:
                i += 1
            self.drawNewLine(thisLine, i)
            lastLine = thisLine
            time.sleep(2.5)
        
    def drawNewLine(self, line, y, x=0):
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.A_UNDERLINE)
        self.refresh()
        
    def drawLine(self, line, y, x=0):
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.color_pair(0))
        self.refresh()
        
    def refresh(self):
        self.screen.refresh()

class InputThread(Thread):
    def __init__(self, screen):
        Thread.__init__(self, name="InputThread")
        self.screen = screen
        
    def run(self):
        while True:
            c =  self.screen.getch()
            if c == 'q':
                print 'q got'
        
if __name__ == '__main__':
    #Main program bits
    if len(sys.argv) > 1:
        if sys.argv[1] == 'book':
            book = Book('example.txt')
            for i in range(30):
                print book.line()
                
        if sys.argv[1] == 'history':
            history = BookHistory()
            history.setBookFile('example.txt')
            history.read()
            print 'line number:', history.lineNumber()
            history.incrementLineNumber()
            history.write()
            
    else:
        def main(stdscr):
            return BookReader(stdscr)
        
        curses.wrapper(main)
    
