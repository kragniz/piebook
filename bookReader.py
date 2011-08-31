#!/usr/bin/env python
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
        '''Return True if the length of line is not larger than the maximum
        length of the line'''
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
    
    def setPosition(self, pos):
        '''Set the position in the book'''
        self.text.seek(pos)
        
    def position(self):
        '''Get the position in the book'''
        return self.text.tell()
        
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
            'position' : 0,
            'speed' : 2.5}
            
    def setBookFile(self, bookFileName):
        '''Set the filename of the book/text document'''
        self._historyData['bookFileName'] = bookFileName
        
    def setPosition(self, n):
        '''Set the current position in the book/text document in bytes'''
        self._historyData['position'] = n
        
    def setSpeed(self, s):
        '''Set the delay between each line re-draw in seconds'''
        self._historyData['speed'] = s
        
    def speed(self):
        '''Return the delay between each line re-draw in seconds'''
        return self._historyData['speed']
        
    def position(self):
        '''Return the current position in the book/text document in bytes'''
        return self._historyData['position']

    def read(self, historyFileName=None):
        '''Read the settings made from a previous run of this program'''
        if not historyFileName:
            historyFileName = splitext(self._historyData['bookFileName'])[0] + '.hst'
        try:
            data = ''.join(open(historyFileName).readlines())
            self._historyData = json.loads(data)
            return True
        except:
            return False
        
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
        bookName = 'example.txt'
        self.screen = screen
        
        self.book = Book(bookName)
        self.history = BookHistory()
        self.history.setBookFile(bookName)
        self.history.read()
        self.book.setPosition(self.history.position())
        
        self.exitObject = Exit()
        self.inputThread = InputThread(self.screen, self.exitObject)
        self.inputThread.start()
        
        self._paused = False
        
        curses.curs_set(0)
        self.screen.timeout(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        
        self.i = 0
        lastLine = ''
        t1 = 0
        try:
            while not self.exitObject.stopping():
                key = self.inputThread.read()
                if key == 32: #space character
                    self.togglePaused()
                    t1 = 0
                    self.showMessage('PAUSED', 'green')
                    
                elif key == 258: #key down
                    t1 = 0
                    
                elif key == 43: #'+'
                    self.history.setSpeed(self.history.speed() + 0.1)
                    self.showMessage('SPEED IS NOW %s' % self.history.speed() , 'green')
                    
                elif key == 45: #'-'
                    self.history.setSpeed(self.history.speed() - 0.1)
                    self.showMessage('SPEED IS NOW %s' % self.history.speed() , 'green')
                
                if not self.paused():
                    if time.time()-t1 >= self.history.speed():
                        t1 = time.time()
                        thisLine = self.book.line()
                        self.drawLine(lastLine)
                        if self.i + 2 >= curses.LINES:
                            self.i = 0
                        else:
                            self.i += 1
                        self.drawNewLine(thisLine)
                        lastLine = thisLine
                time.sleep(0.1) #try to save some cpu cycles
        finally:
            #always stop the thread
            self.inputThread.stop()
            self.history.setPosition(self.book.position())
            self.history.write()
 
    def showMessage(self, message, style='reverse'):
        '''Show a message on the current line. Style can be 'red', 'green' for
        colour, anything else for reverse video'''
        x = curses.COLS - len(message) - 3
        if style == 'red':
            styleArgument = curses.color_pair(1)
        elif style == 'green':
            styleArgument = curses.color_pair(2)
        else:
            styleArgument = curses.A_REVERSE
        self.screen.addstr(self.i, x, ' ' + message + ' ', styleArgument)
        self.refresh()
		
    def drawNewLine(self, line, y=None, x=0):
        '''Draw a line of underlined text'''
        if y == None:
            y = self.i
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.A_UNDERLINE)
        self.refresh()
        
    def drawLine(self, line, y=None, x=0):
        '''Draw a line of normal text'''
        if y == None:
            y = self.i
        self.screen.addstr(y, x, line[:curses.COLS-1].ljust(curses.COLS), curses.color_pair(0))
        self.refresh()
        
    def refresh(self):
        '''Refresh the terminal'''
        self.screen.refresh()
        
    def togglePaused(self):
        '''Pause or un-pause the scrolling of text'''
        self._paused = not self._paused
        
    def paused(self):
        '''Return True if scrolling is paused'''
        return self._paused
        
class Exit(object):
    '''A class to signal when to stop the main program'''
    def __init__(self):
        self._stopping = False
        
    def stop(self):
        '''Signal to stop the program at the next convenient moment'''
        self._stopping = True
        
    def stopping(self):
        '''Return True if the program is stopping'''
        return self._stopping
        
        
class InputThread(Thread):
    '''A thread for taking input from keyboard'''
    def __init__(self, screen, exitObject):
        '''Create thread'''
        Thread.__init__(self, name="InputThread")
        self.screen = screen
        self.exitObject = exitObject
        self._running = True
        self.key = ''
        
    def run(self):
        '''Run the thread. Do not call this directly, use InputThread.start()'''
        while self._running:
            time.sleep(0.05)
            c =  self.screen.getch()
            if c != -1:
                self.key = c
            if self.key == 113 or self.key == 81: #'q' or 'Q'
                self.stop() #stop the thread
                self.exitObject.stop() #stop the main program
            
    def stop(self):
        '''Stop the thread from running'''
        self._running = False
        
    def read(self):
        '''Return the last pressed key'''
        key = self.key
        self.key = ''
        return key
        
if __name__ == '__main__':
    '''Main program bits'''
    #TODO Add command line options
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
        curses.wrapper(main) #use the safe curses wrapper in case things get bad
