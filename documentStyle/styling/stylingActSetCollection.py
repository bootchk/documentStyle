'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from ..styling.stylingActSet import StylingActSet

class StylingActSetCollection(dict):
  '''
  A collection of StylingActSet.
  
  Class invariant: unique on selector (a dictionary.)
  
  Many StylingActSet's may apply to a selector.  E.G. (*,*,*,Color) and (*,*,Pen,Color) both apply to (*,*,Pen,*).
  The first is more selective.
  
  Responsibility:
  - key on unique selector
  - iterate by order of selectivity (TODO)
  '''

  def put(self, stylingActSet):
    self[stylingActSet.selector()] = stylingActSet
  
  def getOrNew(self, selector):
    '''
    StylingActSet that matches, or a new one.
    '''
    if selector in self:
      result = self[selector]
    else:
      result = StylingActSet(selector) # Empty of StylingAct
      self.put(result)
    return result
  
    
  def generateMatchingStylingActSets(self, selector):
    '''
    StylingActSet's (zero or many) that match selector, in order of selectivity.
    '''
    # TODO order by selectivity
    for (selector, stylingActSet) in self.items():
      yield stylingActSet
        