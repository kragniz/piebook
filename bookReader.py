#/usr/bin/env python
#A small text-based ebook reader

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
        '''Split a string into substrings. much simpler than Str.split(), keeps whitespace.'''
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
                
        if not self.w:
            if self._checkLength(''.join(line)):
                words = self._split(self._nextLine())
                while self._checkLength(''.join(line)) and words:
                    line += [words.pop(0)]
            else:
                self.w = [line.pop(-1)] + self.w
                
            if not self._checkLength(''.join(line)):
                self.w = [line.pop(-1)] + self.w
                
            self.w += words
        return ''.join(line)
            
    def _nextLine(self):
        '''Return a single line from the book'''
        return self.text.readline()
    
class BookHistory(object):
    '''Make and write the settings/progress for a particular book'''
    def __init__(self):
        pass
    
class BookReader(object):
    '''Display the book in a terminal'''
    def __init__(self):
        pass
    
if __name__ == '__main__':
    #Main program bits
    book = Book('example.txt')
    for i in range(30):
        print book.line()
    
