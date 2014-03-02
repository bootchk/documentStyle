'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
from documentStyle.debugDecorator import report, reportReturn, reportTrueReturn


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
  
  """
  def __repr__(self):
    ''' !!! Short: is missing dictionary values. '''
    return "StylingActSet(" + str(self.selector) + ")"
  """
  
  #@report
  def applyToFormation(self, formation):
    for stylingAct in self.values():
      # DEBUG uncomment this to see cascade in action
      #print "Applying StylingAct" + str(self)
      stylingAct.applyToFormation(formation)
      
  @reportReturn
  def put(self, stylingAct):
    ''' Add a styling act, or replace an existing one !!! '''
    """
    selector = stylingAct.selector
    if selector in self:
      print("replacing")
    else:
      print("adding")
    """
    self[stylingAct.selector] = stylingAct
    
  @report
  def delete(self, selector):
    '''
    Delete where precondition: selector exists.
    Raise KeyError if not exist.
    '''
    del self[selector]
    
    
  @reportTrueReturn
  def deleteIfExists(self, selector):
    '''
    Same as above but does not raise KeyError.
    '''
    # For DEBUG, return whether deleted.
    try:
      del self[selector]
      return True
    except KeyError:
      # Doesn't exist
      # DEBUG uncomment this to see no styling act deleted for a selector.
      #print "No styling act deleted for selector", selector
      return False
    
    
  def generateStylingActs(self):
    for each in self.values():
      yield each
      

  def countStylingActs(self):
    '''
    Count is total of my stylingActs.
    '''
    total = 0
    for stylingAct in self.itervalues():
      total += 1
    return total
    