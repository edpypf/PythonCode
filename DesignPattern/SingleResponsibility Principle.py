class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0
    
    def add_entries(self,text):
        """append text into entries"""
        self.entries.append(f'{self.count}: {text}')
        self.count += 1

    def remove_entries(self, pos):
        """remove an entries based on the pos"""
        del self.entries[pos]
        self.count -= 1

    def __str__(self):
        """to return all the elements from the list"""
        return '\n'.join(self.entries)
    
    # def save(self, filename):
    #     """ This is where it will against the single repsonsibility rules,
    #         in which the other type of functions would be added to make the class
    #         long and really messed up with inheritance and will be complicated
    #         when the application grow and difficult to expand and maintain
    #         ******************************** Solution ***********************************
    #         ***and normally we will put all these type of functions into another class***
    #     """
    #     file = open(filename, 'w')
    #     file.write(str(self))
    #     file.close
    
    # def load(self, filename):
    #     pass

    # def other(self, uri):
    #     pass

class PersistenceManager:
    @staticmethod
    def save(journal, filename):
        """ This is where it will against the single repsonsibility rules,
            in which the other type of functions would be added to make the class
            long and really messed up with inheritance and will be complicated
            when the application grow and difficult to expand and maintain
            ******************************** Solution ***********************************
            ***and normally we will put all these type of functions into another class***
        """
        file = open(filename, 'w')
        file.write(str(journal))
        file.close

j = Journal()    
j.add_entries('what is the test doing about')
j.add_entries('wish everything would be fine and no issues what so ever')
j.add_entries('Saturday after would be a nice and great week')
j.remove_entries(0)

file = r'c:\temp\journal.txt' ## if Error: No Such file, is due to no Folder created
PersistenceManager.save(j, file)

with open(file, 'r') as f:
    print(f.read())
        
    
