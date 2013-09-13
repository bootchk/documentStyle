'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from documentStyle.debugDecorator import reportReturn


class StylingActSet(dict):
  '''
  Dictionary of StylingActs, keyed by StylingAct.selector
  
  Has-a selector, which identifies what type of Formation it applies to
  
  Since dictionary, only one StylingAct will apply to selected StyleProperty of a Formation.
  But one StylingAct may apply to many StyleProperties of a Formation (when the selector has wildcard.)
  
  A unit of editing: StylingActs are grouped by StylingActSet
  
  Responsibilities:
  - apply to Formation, modifying it
  - contain StylingActs
  - know selector
  - know name (TODO subclass NamedStylingActSet)
  '''
  
  def __init__(self, selector):
    self.selector = selector
  
  def __repr__(self):
    ''' !!! Short: is missing dictionary values. '''
    return "StylingActSet(" + str(self.selector) + ")"
  
  #@report
  def applyToFormation(self, formation):
    for stylingAct in self.values():
      #print "From StylingActSet " + str(self)
      stylingAct.applyToFormation(formation)
      
  @reportReturn
  def put(self, stylingAct):
    ''' Add a styling act, or replace an existing one !!! '''
    self[stylingAct.selector] = stylingAct
    
    
  def delete(self, selector):
    '''
    Delete where precondition: selector exists.
    Raise KeyError if not exist.
    '''
    del self[selector]
    
    
  @reportReturn
  def deleteIfExists(self, selector):
    '''
    Same as above but does not raise KeyError.
    '''
    # For debugging purposes, return whether deleted.
    try:
      del self[selector]
      return True
    except KeyError:
      # Doesn't exist
      # print "No styling act deleted for selector", selector
      return False
