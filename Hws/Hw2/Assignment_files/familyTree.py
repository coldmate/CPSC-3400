"""
GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointers to Family object
Skip other lines

Testing to show the data structures:
    Print info from the collections of Person and Family objects
    Print descendant chart after all lines are processed

"""

from collections import namedtuple

#-----------------------------------------------------------------------

class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self,ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._events = []
                
    def addName(self, names):
        # Extracts name parts from a list of names and stores them
        self._given = names[0]
        self._surname = names[1]
        self._suffix = names[2]

    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse.append(famRef)
        
    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef

    def addEvent(self, newEvent):
        # Adds a new event and stores it into event list
        self._events.append(newEvent)

    def printDescendants(self, prefix=''):
        # print info for this person and then call method in Family
        print(prefix + self.name() + self.eventInfo())
        # recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def isDescendant(self, personID):
        # Returns true if the person is a descendant of self
        if self._id == personID:
            return True

        # Each spouse from each family
        for fam in self._asSpouse:
            # Each child from each spouse
            for child in families[fam]._children:
                # Call isDecendant on the child
                if(persons[child].isDescendant(personID)):
                    # Returns true if child is an descendant
                    return True
        #Returns false if an descendant is not found 
        return False
    
    def printAncestors(self, prefix=''): # going up the tree
        # Prints out the ancestors of self 
        if prefix == "":
            prefix = '0'

        # If self is part of the family as a child
        if(self._asChild):
            # For every spouse in the family
            family = getFamily(self._asChild)

            if(family):
                nextPrefix = int(prefix) + 1
                parent1 = getPerson(family._spouse1[0])
                parent2 = getPerson(family._spouse2[0])
                
                if(parent1):
                    parent1.printAncestors(str(nextPrefix))
                    
                spaces = "";
                for i in range(nextPrefix - 1):
                    spaces += " ";
                    
                print(spaces + prefix, self.name(), self.eventInfo())
                
                if(parent2):
                    parent2.printAncestors(str(nextPrefix))
            else:
                print(prefix, self.name(), self.eventInfo())

        parents  = self.getParents()
        if not parents: 
            print(" " * int(prefix), prefix, self.name(), self.eventInfo())
        
    def printCousins(self, n=1):
        if n == 1:
            self.printFirstCousins()
        elif n == 2:
            self.printSecondCousins()
        elif n ==  3:
            self.printThirdCousins()
        else:
            print("Invalid value of n. Only 1, 2, or 3 are supported.")

    def printFirstCousins(self):
        print("First cousins of", self.name())

        if(self._asChild):
            #parents = []
            auncles = [] # list of parents siblings
            cousins = [] # a list of parents siblings children

        # get parents
            parents  = self.getParents()
        
        # get parent siblings
            if(parents) :
                for parent in parents:
                    auncles += parent.getSiblings()
            else:
                print("No cousins.")
    
        # get parents sibling children
            if(auncles) :
                for sibling in auncles:
                    cousins += sibling.getChildren()
            else: 
              print("No cousins.")
          
        # if there is cousins, print them out
            if (cousins):
                for cousin in cousins:
                    print(cousin.name(), cousin.eventInfo())
            else:
                print("No cousins.") 
        else:
            print("No cousins.")

    def printSecondCousins(self):
        print("Second cousins of", self.name())

        grandParents = []
        grandAUncles = []
        FCOR = []
        secondCousins = []

        parents = self.getParents()
        if(parents):
                for parent in parents:
                    grandParents += parent.getParents()
                    
        if(grandParents):
            for grandParent in grandParents:
                grandAUncles += grandParent.getSiblings()

        if(grandAUncles):
            for grandAUncle in grandAUncles:
                FCOR += grandAUncle.getChildren()

        if(FCOR):
            for cousin in FCOR:
                secondCousins += cousin.getChildren()
        
        if (secondCousins):
            for cousin in secondCousins:
                print(cousin.name(), cousin.eventInfo())
        else:
            print("No cousins.")

    def printThirdCousins(self):
        print("Third cousins of", self.name())

        greatGrandParents = []
        grandParents = []
        FCTR = []
        SCOR = []
        thirdCousins = []

        parents = self.getParents()
        if(parents):
                for parent in parents:
                    grandParents += parent.getParents()
        else:
                print("No cousins.")
                
        if(grandParents):
            for grandParent in grandParents:
                greatGrandParents += grandParent.getParents()
        else:
                print("No cousins.")

        if(greatGrandParents):
            for greatGrandParent in greatGrandParents:
                FCTR += greatGrandParent.getSiblings()
        else:
                print("No cousins.")

        if(FCTR):
            for secondCousin in FCTR:
                SCOR += secondCousin.getChildren()
        else:
                print("No cousins.")

        if(SCOR):
            for cousin in SCOR:
                thirdCousins += cousin.getChildren()
        else:
                print("No cousins.")

        if (thirdCousins):
            for cousin in thirdCousins:
                print(cousin.name(), cousin.eventInfo())
        else:
            print("No cousins.")
        
    
    def getParents(self):
      # returns a list of Persons that are parents of self
        parents = []
        if(self._asChild):
            family = getFamily(self._asChild)
            parent1 = getPerson(family._spouse1[0])
            parent2 = getPerson(family._spouse2[0])
            if(parent1):
                parents.append(parent1)
                if(parent2):
                    parents.append(parent2)
            else:
              parents.append(parent2)
        return parents
    
    def getSiblings(self):
        siblings = []
        if(self._asChild):
            family = getFamily(self._asChild)
            for childRef in family._children:
                child = getPerson(childRef)
                if(child._id != self._id):
                    siblings.append(child)
        return siblings

    def getChildren(self):
        children = []
        if(self._asSpouse):
        # for every family self is a spouse
            for famRef in self._asSpouse: 
                family = getFamily(famRef)
                for childRef in family._children:
                    children.append(getPerson(childRef))
        return children
 
    def name (self):
        # returns a simple name string 
        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix
    
    def treeInfo (self):
        # returns a string representing the structure references included in self
        if self._asChild: # make sure value is not None
            childString = ' | asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            # Use join() to put commas between identifiers for multiple families
            # No comma appears if there is only one family on the list
            spouseString = ' | asSpouse: ' + ','.join(self._asSpouse)
        else: spouseString = ''
        return childString + spouseString
                
    def eventInfo(self):
        ## add code here to show information from events once they are recognized
        eventStr = ''
        for event in self._events:
            eventStr += (" | " + str(event))
        return eventStr

    def __str__(self):
        # Returns a string representing all info in a Person instance
        # When treeInfo is no longer needed for debugging it can 
        return self.name() \
                + self.eventInfo()  \
                + self.treeInfo()  ## Comment out when not needed for debugging

    

# end of class Person
 
#-----------------------------------------------------------------------

# Declare a named tuple type used by Family to create a list of spouses
Spouse = namedtuple('Spouse',['personRef','tag'])

class Family():
    # Stores info about a family
    # An instance is created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------


    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._spouse1 = None
        self._spouse2 = None
        self._children = []
        self._events = []

    def addSpouse(self, personRef, tag):
        # Stores the string (personRef) indicating a spouse in this family
        newSpouse = Spouse(personRef, tag)
        if self._spouse1 == None:
            self._spouse1 = newSpouse
        else: self._spouse2 = newSpouse

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children.append(personRef)

    def addEvent(self, newEvent):
        self._events.append(newEvent)
        
    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print other spouse
        # and recursively invoke printDescendants on children

        # Manipulate prefix to prepare for adding a spouse and children
        if prefix != '': prefix = prefix[:-2]+'  '
        
        # Print out a '+' and the name of the second spouse, if present
        if self._spouse2:  # check for the presence of a second spouse
            # If a second spouse is included, figure out which is the
            # "other" spouse relative to the descendant firstSpouse
            if self._spouse1.personRef == firstSpouse:
                secondSpouse = self._spouse2.personRef
            else: secondSpouse = self._spouse1.personRef
            #print(prefix+ '+' + persons[secondSpouse].name())
            marrEvents = ''
            for event in self._events:
                marrEvents += " | " + str(event)
            print(prefix+ '+' + persons[secondSpouse].name() + marrEvents)

        # Make a recursive call for each child in this family
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')
        
    def __str__(self):
        ## Constructs a single string including all info about this Family instance
        spousePart = ''
        for spouse in (self._spouse1, self._spouse2):  # spouse will be a Spouse namedtuple (spouseRef,tag)
            if spouse:  # check that spouse is not None
                if spouse.tag == 'HUSB':
                    spousePart += ' Husband: ' + spouse.personRef
                else: spousePart += ' Wife: ' + spouse.personRef
        childrenPart = '' if self._children == [] \
            else' Children: ' + ','.join(self._children)
        return spousePart + childrenPart

# end of class Family

#-----------------------------------------------------------------------
class Event():
    def __init__(self):
        self._date = ""
        self._place = ""

    def addDate(self, newDate):
        self._date = newDate

    def addPlace(self, newPlace):
        self._place = newPlace

    def __str__(self):
        eventParts = (self._date + " " + self._place + " ")
        return eventParts

# end of class Event

#-----------------------------------------------------------------------
# Global dictionaries used by Person and Family to map INDI and FAM identifier
# strings to corresponding object instances

persons = dict()  # saves references to all of the Person objects
families = dict() # saves references to all of the Family objects

## Access functions to map identifier strings to Person and Family objects
## Meant to be used in a module that tests this one

def getPerson (personID):
    return persons[personID]

def getFamily (familyID):
    return families[familyID]

## Print functions that print the info in all Person and Family objects 
## Meant to be used in a module that tests this one
def printAllPersonInfo():
    # Print out all information stored about individuals
    for ref in sorted(persons.keys()):
        print(ref + ':' + str(persons[ref]))
    print()

def printAllFamilyInfo():
    # Print out all information stored about families
    for ref in sorted(families.keys()):
        print(ref + ':' + str(families[ref]))
    print()

#-----------------------------------------------------------------------
 
def processGEDCOM(file):

    def getPointer(line):
        # A helper function used in multiple places in the next two functions
        # Depends on the syntax of pointers in certain GEDCOM elements
        # Returns the string of the pointer without surrounding '@'s or trailing
        return line[8:].split('@')[0]
            
    def processPerson(newPerson):
        nonlocal line
        line = f.readline()
        while line[0] != '0': # process all lines until next 0-level
            tag = line[2:6]  # substring where tags are found in 0-level elements
            if tag == 'NAME':
                names = line[6:].split('/')  #surname is surrounded by slashes
                names[0] = names[0].strip()
                names[2] = names[2].strip()
                newPerson.addName(names)
            elif tag == 'FAMS':
                newPerson.addIsSpouse(getPointer(line))
            elif tag == 'FAMC':
                newPerson.addIsChild(getPointer(line))
            ## add code here to look for other fields
            elif(tag == 'BIRT'):
                line = f.readline()
                newEvent = Event()
                tag = line[2:6]
                data = line[7:]
                if(tag == 'DATE'):
                    newEvent.addDate("n: " + data.strip())
                    line = f.readline()
                    tag = line[2:6]
                    data = line[7:]
                    if(tag == 'PLAC'):
                        newEvent.addPlace(data.strip())
                    elif(tag == 'PLAC'):
                        newEvent.addPlace(data.strip())
                newPerson.addEvent(newEvent)
            elif(tag == 'DEAT'):
                line = f.readline()
                newEvent = Event()
                tag = line[2:6]
                data = line[7:]
                if(tag == 'DATE'):
                    newEvent.addDate("d: " + data.strip())
                    line = f.readline()
                    tag = line[2:6]
                    data = line[7:]
                    if(tag == 'PLAC'):
                        newEvent.addPlace(data.strip())
                    elif(tag == 'PLAC'):
                        newEvent.addPlace(data.strip())
                newPerson.addEvent(newEvent)

            # read to go to next line
            line = f.readline()

    def processFamily(newFamily):
        nonlocal line
        line = f.readline()
        while line[0] != '0':  # process all lines until next 0-level
            tag = line[2:6]
            if tag == 'HUSB':
                newFamily.addSpouse(getPointer(line),'HUSB')
            elif tag == 'WIFE':
                newFamily.addSpouse(getPointer(line),'WIFE')
            elif tag == 'CHIL':
                newFamily.addChild(getPointer(line))
            ## add code here to look for other fields

            elif(tag == 'MARR'):
                line = f.readline()
                newEvent = Event()
                tag = line[2:6]
                if(tag == 'DATE'):
                    newEvent.addDate(":m " + line[7:].strip())
                    tag = line[2:6]
                    if(tag == 'PLAC'):
                        newEvent.addPlace(line[7:].strip())
                elif(tag == 'PLAC'):
                    newEvent.addPlace(line[7:].strip())
                newFamily.addEvent(newEvent)
                

            # read to go to next line
            line = f.readline()


    ## f is the file handle for the GEDCOM file, visible to helper functions
    ## line is the "current line" which may be changed by helper functions

    f = open (file)
    line = f.readline()
    while line != '':  # end loop when file is empty
        fields = line.strip().split(' ')
        # print(fields)
        if line[0] == '0' and len(fields) > 2:
            # print(fields)
            if (fields[2] == "INDI"): 
                ref = fields[1].strip('@')
                ## create a new Person and save it in mapping dictionary
                persons[ref] = Person(ref)
                ## process remainder of the INDI record
                processPerson(persons[ref])
                
            elif (fields[2] == "FAM"):
                ref = fields[1].strip('@')
                ## create a new Family and save it in mapping dictionary
                families[ref] = Family(ref) 
                ## process remainder of the FAM record
                processFamily(families[ref])
                
            else:    # 0-level line, but not of interest -- skip it
                line = f.readline()
        else:    # skip lines until next candidate 0-level line
            line = f.readline()

    ## End of ProcessGEDCOM

#-----------------------------------------------------------------------    
## Test code starts here
            
def _main():
    filename = "Kennedy.ged"  # Set a default name for the file to be processed
##    Uncomment the next line to make the program interactive
##    filename = input("Type the name of the GEDCOM file:")

    processGEDCOM(filename)

    printAllPersonInfo()

    printAllFamilyInfo()
    
    person = "I46"  # Default selection to work with Kennedy.ged file
##    Uncomment the next line to make the program interactive
##    person = input("Enter person ID for descendants chart:")

    getPerson(person).printDescendants()
    
if __name__ == '__main__':
    _main()

