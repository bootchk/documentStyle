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
    '''
  
  __slots__ = ()  # Eliminate per instance dictionary
  
  
  def __repr__(self):
    return "Selector(" + self.name + "," + self.DEType + "," + self.instrument + "," + self.field + ")"
  
  
  def matches(self, other):
    return ( self.name == other.name or other.name == "*" or self.name == "*" ) \
      and  ( self.DEType == other.DEType or other.DEType == "*" or self.DEType == "*" ) \
      and  ( self.instrument == other.instrument or other.instrument == "*" or self.instrument == "*" ) \
      and  ( self.field == other.field or other.field == "*" or self.field == "*")

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

