#/usr/bin/env python
#A small text-based ebook reader

class Book(object):
    '''Handle reading and manipulating lines from a text file'''
    def __init__(self, textFileName):
        '''Create a book object'''
        self.lineLength = 80
        text = open(textFileName, 'r')
        
        self.continuedLine = ''
        
    def setLineLength(self, length):
        '''Set the length of each line of the output'''
        self.lineLength = length
        
    def _checkLength(self, line):
        return (len(line) <= self.lineLength)
    
    def line(self):
        '''Return the next line'''
        line = ''
            
    def _nextLine(self):
        '''Return a single line from the book'''
        return text.read()
    
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
