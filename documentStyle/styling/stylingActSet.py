'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
#from documentStyle.debugDecorator import report


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
    return "StylingActSet(" + str(self.selector) + ")"
  
  #@report
  def applyToFormation(self, formation):
    for stylingAct in self.values():
      #print "From StylingActSet " + str(self)
      stylingAct.applyToFormation(formation)
      
  def put(self, stylingAct):
    self[stylingAct.selector] = stylingAct
    
  def delete(self, selector):
    del self[selector]
