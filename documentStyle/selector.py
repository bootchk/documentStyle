'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from collections import namedtuple


class Selector(namedtuple('Selector', 'name DEType instrument field')):
  '''
    Data structure for selecting various style objects.
    
    Superclass of a namedtuple.  See Python docs for collections.namedtuple
    
    Responsibility:
    - hashable (immutable tuple)
    - match self to other
    - knows selectivity (TODO)
    
    See testSelector.txt for docTest tests.
    '''
  
  __slots__ = ()  # Eliminate per instance dictionary
  
  
  def __repr__(self):
    return "Selector(" + self.name + "," + self.DEType + "," + self.instrument + "," + self.field + ")"

  
  def noncommutativeMatches(self, other):
    ''' Non-commutative: self more selective than other raises exception. '''
    assert other.isAtLeastSelectiveAs(self), str(self) + str(other)
    return ( self.name == other.name or self.name == "*" ) \
      and  ( self.DEType == other.DEType or self.DEType == "*" ) \
      and  ( self.instrument == other.instrument or self.instrument == "*" ) \
      and  ( self.field == other.field or self.field == "*")

  def commutativeMatches(self, other):
    ''' Loosely speaking, self.matches(other) or other.matches(self.), not raising exception about relative selectivity. '''
    return ( self.name == other.name or other.name == "*" or self.name == "*" ) \
      and  ( self.DEType == other.DEType or other.DEType == "*" or self.DEType == "*" ) \
      and  ( self.instrument == other.instrument or other.instrument == "*" or self.instrument == "*" ) \
      and  ( self.field == other.field or other.field == "*" or self.field == "*")
    
  def matchesToInstrument(self, other):
    '''  '''
    ## Name is not implemented, always "*"
    ## if self.name == other.name:
    '''
    !!! Note asymmetry: self DEType == * matches other, but other.instrument == * matches self
    Self is selector of a StylingAct and other is selector of a formation.
    '''
    if self.DEType == other.DEType or self.DEType == '*':
      if self.instrument == other.instrument or other.instrument == '*':
        return True
    return False
  
    
  def isAnyDETypeAndInstrumentSelector(self):
    ''' Selects a particular instrument for any DEType. '''
    return self.DEType == '*' and self.instrument != '*' and self.field == '*'
  
  def isDETypeSelector(self):
    ''' Selects all instruments for a DEType. '''
    return self.DEType != '*' and self.instrument == '*'
  
  def isDETypeAndInstrumentSelector(self):
    ''' Selects particular instrument for particular DEType. '''
    return self.DEType != '*' and self.instrument != '*'
  
  '''
  Selectivity.
  '''
  def isAtLeastSelectiveAs(self, other):
    return self.selectivityCount() <= other.selectivityCount()
  
  def selectivityCount(self):
    ''' Count leading i.e. prefix '*' '''
    count = 0
    if self.name == '*': 
      count +=1
      if self.DEType == '*':
        count +=1
        if self.instrument == '*':
          count +=1
          if self.field == '*':
            count +=1
    return count
      
    
'''
Constructors of subtypes (by data, not by subclass)
'''
    
def newAllSelector():
  ''' New copy of universal selector. '''
  return Selector("*", "*", "*", "*")

def DETypeSelector(DEType):
  return Selector("*", DEType, "*", "*")

def instrumentSelector(source, instrumentName):
  ''' Derive from source, substitute instrumentName for instrument field. '''
  return Selector(source.name, source.DEType, instrumentName, source.field)

def fieldSelector(source, fieldName):
  ''' Derive from source, substitute fieldName for 'field' field. '''
  return Selector(source.name, source.DEType, source.instrument, fieldName)

