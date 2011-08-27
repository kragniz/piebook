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
                
            if not self._checkLength(''.join(line)):
                self.w = [line.pop(-1)] + self.w
                
            self.w += words
        
        return ''.join(line).replace('\n', '')
            
    def _nextLine(self):
        '''Return a single line from the book'''
        return self.text.readline()
    
class BookHistory(object):
    '''Make and write the settings/progress for a particular book'''
    def __init__(self):
        pass
    
class BookReader(object):
    '''Display the book in a terminal'''
    def __init__(self, screen):
        self.screen = screen
        self.book = Book('example.txt')
        
        curses.curs_set(0)
        self.cols = curses.COLS
        self.rows = curses.LINES
        i = 0
        di = 1
        while True:
            if i+1 >= self.rows:
                di = -di
            elif i-1 == 0 and di < 0:
                di = -di
            
            i += di
            
            self.drawReverseLine('hello', i)
            if (i-5) > 0 and di > 0:
                self.drawLine('     ', i-5)
            elif (i+5) < self.rows and di < 0:
                self.drawLine('     ', i+5)
            time.sleep(0.02)
        
    def drawReverseLine(self, line, y, x=0):
        self.screen.addstr(y, x, line, curses.A_REVERSE)
        self.refresh()
        
    def drawLine(self, line, y, x=0):
        self.screen.addstr(y, x, line)
        self.refresh()
        
    def refresh(self):
        self.screen.refresh()

if __name__ == '__main__':
    #Main program bits
    def main(stdscr):
        #foreground/background colour pair
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
        return BookReader(stdscr)
    
    curses.wrapper(main)
    
