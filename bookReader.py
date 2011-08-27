#/usr/bin/env python
#A small text-based ebook reader

class Book(object):
    '''Handle reading and manipulating lines from a text file'''
    def __init__(self, textFileName):
        '''Create a book object'''
        self.lineLength = 80
        self.text = open(textFileName, 'r')
        
        self.continuedWords = []
        
    def setLineLength(self, length):
        '''Set the length of each line of the output'''
        self.lineLength = length
        
    def _checkLength(self, line):
        return (len(line) <= self.lineLength)
    
    def line(self):
        '''Return the next line'''
        line = []
        words = []
        
        if self.continuedWords:
            while self._checkLength(' '.join(line)) and self.continuedWords:
                line += [self.continuedWords.pop(0)]
                
        if self._checkLength(' '.join(line)):
            words = self._nextLine().split()
            while self._checkLength(' '.join(line)) and words:
                line += [words.pop(0)]
        else:
            self.continuedWords = [line.pop(-1)] + self.continuedWords
            
        if not self._checkLength(' '.join(line)):
            self.continuedWords = [line.pop(-1)] + self.continuedWords
            
        self.continuedWords += words
        return ' '.join(line)
            
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
    print book.line()
    print book.line()
    print book.line()
    print book.line()
    print book.line()
