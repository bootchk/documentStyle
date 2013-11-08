'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import QCoreApplication
from .intermediateStyleSheet import IntermediateStyleSheet
from documentStyle.styling.stylingActSet import StylingActSet


class DocumentElementStyleSheet(IntermediateStyleSheet):
  '''
  StyleSheet attached to a DocumentElement.
  
  Specializes StyleSheet:
  - leaf. No NamedStylingActSet since nothing can refer to it (Design might change.)
  - ALWAYS parented to docStyleSheet
  - name is generic (not a user-given name to instance)
  '''
  def __init__(self, name):
    IntermediateStyleSheet.__init__(self, name)
    '''
    Reimplement: Always parented to docStyleSheet.
    
    assert app has docStyleSheet attribute, i.e. parent style sheet exists.
    Note that when unpickling a document, its docStyleSheet must be unpickled first.
    '''
    self.setParent(QCoreApplication.instance().cascadion.docStyleSheet)
    
    
  def generateStylingActs(self, selector):
    for each in self.stylingActSet(selector).generateStylingActs():
      yield each
    
    
  def stylingActSet(self, selector):
    '''
    Return existing SAS, or lazily create empty SAS.
    
    Note that a styleSheet doesn't have a selector, one must be passed.
    '''
    assert selector.isDETypeSelector()
    # Invariant, DSS has only zero or one SAS.
    assert len(self.stylingActSetCollection) <= 1
    ''' Lazy '''
    if len(self.stylingActSetCollection) == 0:
      self.stylingActSetCollection.putNewBySelector(selector)
    else:
      # Already exists, and its selector matches the one passed
      assert self.stylingActSetCollection.values()[0].selector == selector
      pass
    assert len(self.stylingActSetCollection) == 1
    result = self.stylingActSetCollection.values()[0]
    assert isinstance(result, StylingActSet)
    return result
        